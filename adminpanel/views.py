# Import shortcuts used to render pages, redirect users, and fetch objects safely
from django.shortcuts import render, redirect, get_object_or_404

# login_required ensures only logged-in users can access a view
# user_passes_test checks whether the logged-in user passes a custom condition
from django.contrib.auth.decorators import login_required, user_passes_test

# Keeps the user logged in after changing their password
from django.contrib.auth import update_session_auth_hash

# Used to show success/error messages in templates
from django.contrib import messages

# Gets the active User model, including custom user models
from django.contrib.auth import get_user_model

# Import models needed for admin statistics and management
from restaurant.models import Category, Restaurant, Dish
from orders.models import Cart, CartItem


# Store the active user model in a variable
User = get_user_model()


# Custom check to allow only authenticated staff/admin users
def is_admin(user):
    return user.is_authenticated and user.is_staff


# =====================
# DASHBOARD
# =====================
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Count important records for the admin dashboard summary cards
    total_users = User.objects.filter(is_staff=False).count()
    total_restaurants = Restaurant.objects.count()
    total_categories = Category.objects.count()
    total_dishes = Dish.objects.count()

    # Get the 5 newest non-staff users
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]

    # Send all dashboard data to the template
    context = {
        'total_users': total_users,
        'total_restaurants': total_restaurants,
        'total_categories': total_categories,
        'total_dishes': total_dishes,
        'recent_users': recent_users,
    }

    return render(request, 'adminpanel/dashboard.html', context)


# =====================
# CATEGORIES
# =====================
@login_required
@user_passes_test(is_admin)
def categories(request):
    # If the form is submitted, create a new category
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        # Only create category if the name is not empty
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" added successfully.')
        else:
            messages.error(request, 'Category name cannot be empty.')

        # Redirect prevents duplicate form submission on refresh
        return redirect('adminpanel:categories')

    # Get all categories to display on the page
    all_categories = Category.objects.all()

    return render(request, 'adminpanel/categories.html', {
        'categories': all_categories
    })


@login_required
@user_passes_test(is_admin)
def delete_category(request, pk):
    # Find the category by ID, or show 404 if it does not exist
    category = get_object_or_404(Category, pk=pk)

    # Delete the selected category
    category.delete()

    messages.success(request, 'Category deleted.')

    return redirect('adminpanel:categories')


# =====================
# FOOD TYPES
# =====================
@login_required
@user_passes_test(is_admin)
def food_types(request):
    # Fixed list of food type options shown in the admin panel
    FOOD_TYPE_CHOICES = ['Veg', 'Non-Veg', 'Vegan', 'Halal', 'Kosher']

    # Get all dishes with their related category and restaurant in one query
    dishes = Dish.objects.select_related('category', 'restaurant').all()

    return render(request, 'adminpanel/food_types.html', {
        'dishes': dishes,
        'food_type_choices': FOOD_TYPE_CHOICES,
    })


# =====================
# REPORTS
# =====================
@login_required
@user_passes_test(is_admin)
def reports(request):
    # Get data needed for admin reports
    restaurants = Restaurant.objects.all()
    customers = User.objects.filter(is_staff=False)
    carts = Cart.objects.select_related('user').all()

    context = {
        'restaurants': restaurants,
        'customers': customers,
        'carts': carts,
    }

    return render(request, 'adminpanel/reports.html', context)


# =====================
# ORDERS
# =====================
@login_required
@user_passes_test(is_admin)
def orders(request):
    # Get carts with users and cart items efficiently
    all_carts = Cart.objects.select_related('user').prefetch_related('items__dish').all()

    return render(request, 'adminpanel/orders.html', {
        'carts': all_carts
    })


# =====================
# PROFILE
# =====================
@login_required
@user_passes_test(is_admin)
def profile(request):
    # Handle profile update or password change form submission
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user

        # Update admin profile details
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()

            messages.success(request, 'Profile updated successfully.')

        # Change admin password
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            # Check old password first
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')

            # Check that both new passwords match
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')

            else:
                # Save the new password securely
                user.set_password(new_password)
                user.save()

                # Keep user logged in after password change
                update_session_auth_hash(request, user)

                messages.success(request, 'Password changed successfully.')

        return redirect('adminpanel:profile')

    # Display the profile page for GET requests
    return render(request, 'adminpanel/profile.html', {
        'user': request.user
    })