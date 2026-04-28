from django.shortcuts import render  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore

from restaurant.models import Category, Dish
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