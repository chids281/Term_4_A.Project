# Used to render templates, redirect users, and safely get objects
from django.shortcuts import render, redirect, get_object_or_404  # type: ignore

# Ensures only logged-in users can access these pages
from django.contrib.auth.decorators import login_required  # type: ignore

# Used to calculate total money spent
from django.db.models import Sum

# Used to show success/error messages
from django.contrib import messages

# Import models used on customer pages
from restaurant.models import Category, Dish
from orders.models import Cart, Order


# =====================
# CUSTOMER DASHBOARD
# =====================
@login_required
def customer_dashboard(request):
    # Get search text from the search bar, if any
    query = request.GET.get("q")

    # Get all categories for category cards/filters
    categories = Category.objects.all()

    # Start with all dishes
    dishes = Dish.objects.all()

    # If user searched for food, filter dishes by name
    if query:
        dishes = dishes.filter(name__icontains=query)

    # Only show 6 dishes on the dashboard
    dishes = dishes[:6]

    # Default cart count is 0
    cart_count = 0

    # Get the logged-in user's cart, if it exists
    cart = Cart.objects.filter(user=request.user).first()

    # Count total quantity of items in cart
    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())

    return render(request, "customer/dashboard.html", {
        "categories": categories,
        "dishes": dishes,
        "cart_count": cart_count,
    })


# =====================
# CUSTOMER ORDERS PAGE
# =====================
@login_required
def orders(request):
    return render(request, "customer/orders.html")


# =====================
# CUSTOMER PROFILE
# =====================
@login_required
def profile(request):
    # Get all orders for the logged-in user
    orders = Order.objects.filter(user=request.user)

    # Count total orders
    total_orders = orders.count()

    # Add all order totals together
    total_spent = orders.aggregate(total=Sum("total"))["total"] or 0

    # Handle profile update form
    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        request.user.address = address
        request.user.phone = phone
        request.user.save()

        messages.success(request, "Profile updated successfully.")

        # If you add app_name='customer' in customer/urls.py, use:
        # return redirect("customer:profile")
        return redirect("profile")

    return render(request, "customer/profile.html", {
        "total_orders": total_orders,
        "total_spent": total_spent,
    })


# =====================
# PAYMENT PAGE
# =====================
@login_required
def payment(request):
    return render(request, "customer/payment.html")


# =====================
# OFFERS PAGE
# =====================
@login_required
def offers(request):
    return render(request, "customer/offers.html")


# =====================
# HELP CENTER PAGE
# =====================
@login_required
def help_center(request):
    return render(request, "customer/help_center.html")


# =====================
# CATEGORY DISHES PAGE
# =====================
@login_required
def category_dishes(request, category_id):
    # Get selected category or show 404 if it does not exist
    category = get_object_or_404(Category, id=category_id)

    # Get dishes belonging to that category
    dishes = Dish.objects.filter(category=category)

    return render(request, "customer/category_dishes.html", {
        "category": category,
        "dishes": dishes,
    })