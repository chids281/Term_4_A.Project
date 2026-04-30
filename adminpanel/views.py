from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import get_user_model
from restaurant.models import Category, Restaurant, Dish
from orders.models import Cart, CartItem
 
User = get_user_model()
 
def is_admin(user):
    return user.is_authenticated and user.is_staff
 
# =====================
# DASHBOARD
# =====================
@login_required
@user_passes_test(is_admin)
def dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_restaurants = Restaurant.objects.count()
    total_categories = Category.objects.count()
    total_dishes = Dish.objects.count()
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
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
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            Category.objects.create(name=name)
            messages.success(request, f'Category "{name}" added successfully.')
        else:
            messages.error(request, 'Category name cannot be empty.')
        return redirect('adminpanel:categories')
    
    all_categories = Category.objects.all()
    return render(request, 'adminpanel/categories.html', {'categories': all_categories})
 
@login_required
@user_passes_test(is_admin)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, f'Category deleted.')
    return redirect('adminpanel:categories')
 
# =====================
# FOOD TYPE (Dish types via category)
# =====================
@login_required
@user_passes_test(is_admin)
def food_types(request):
    FOOD_TYPE_CHOICES = ['Veg', 'Non-Veg', 'Vegan', 'Halal', 'Kosher']
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
    all_carts = Cart.objects.select_related('user').prefetch_related('items__dish').all()
    return render(request, 'adminpanel/orders.html', {'carts': all_carts})
 
# =====================
# PROFILE
# =====================
@login_required
@user_passes_test(is_admin)
def profile(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user = request.user
 
        if action == 'update_profile':
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            messages.success(request, 'Profile updated successfully.')
 
        elif action == 'change_password':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
 
            if not user.check_password(old_password):
                messages.error(request, 'Old password is incorrect.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
 
        return redirect('adminpanel:profile')
 
    return render(request, 'adminpanel/profile.html', {'user': request.user})