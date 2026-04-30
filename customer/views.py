from django.shortcuts import render,redirect  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from orders.models import Order
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from restaurant.models import Category, Dish
from django.contrib import messages
from orders.models import Cart


@login_required
def customer_dashboard(request):
    query = request.GET.get("q")

    categories = Category.objects.all()
    dishes = Dish.objects.all()

    if query:
        dishes = dishes.filter(name__icontains=query)

    dishes = dishes[:6]

    cart_count = 0
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart_count = sum(item.quantity for item in cart.items.all())

    return render(request, "customer/dashboard.html", {
        "categories": categories,
        "dishes": dishes,
        "cart_count": cart_count,
    })


@login_required
def profile(request):
    return render(request, "customer/profile.html")


@login_required
def orders(request):
    return render(request, "customer/orders.html")

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)

    total_orders = orders.count()

    total_spent = orders.aggregate(
        total=Sum("total")
    )["total"] or 0

    return render(request, "customer/profile.html", {
        "total_orders": total_orders,
        "total_spent": total_spent
    })

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)

    total_orders = orders.count()
    total_spent = orders.aggregate(total=Sum("total"))["total"] or 0

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        request.user.address = address
        request.user.phone = phone
        request.user.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile")

    return render(request, "customer/profile.html", {
        "total_orders": total_orders,
        "total_spent": total_spent,
    })

@login_required
def payment(request):
    return render(request, "customer/payment.html")


@login_required
def offers(request):
    return render(request, "customer/offers.html")


@login_required
def help_center(request):
    return render(request, "customer/help_center.html")

@login_required
def category_dishes(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    dishes = Dish.objects.filter(category=category)

    return render(request, "customer/category_dishes.html", {
        "category": category,
        "dishes": dishes,
    })

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            # Keeps user logged in after password change
            update_session_auth_hash (request, user)

            messages.success(request, "Password changed successfully.")
            return redirect("customer_dashboard")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "customer/change_password.html", {
        "form": form
    })