from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from restaurant.models import Dish
from .models import Cart, CartItem


DELIVERY_FEE = 1000


def get_cart_totals(cart):
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.subtotal() for item in cart_items)
    total = subtotal + DELIVERY_FEE if subtotal > 0 else 0
    cart_count = sum(item.quantity for item in cart_items)

    return cart_items, subtotal, total, cart_count


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': DELIVERY_FEE,
        'total': total,
        'cart_count': cart_count,
    })


@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_count": cart_count,
            "message": f"{dish.name} added to cart",
        })

    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    item.delete()

    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "removed": True,
            "subtotal": subtotal,
            "total": total,
            "cart_count": cart_count,
        })

    return redirect('cart')


@require_POST
@login_required
def update_cart(request, item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    action = request.POST.get("action")
    removed = False

    if action == "increase":
        item.quantity += 1
        item.save()

    elif action == "decrease":
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
            removed = True

    else:
        return JsonResponse({
            "success": False,
            "error": "Invalid action"
        }, status=400)

    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "removed": removed,
            "quantity": 0 if removed else item.quantity,
            "item_total": 0 if removed else item.subtotal(),
            "subtotal": subtotal,
            "total": total,
            "cart_count": cart_count,
        })

    return redirect('cart')


@login_required
def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, dish=dish).first()

    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)

    return render(request, "orders/dish_detail.html", {
        "dish": dish,
        "cart_item": cart_item,
        "cart_count": cart_count,
    })
@login_required
def update_dish_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    action = request.POST.get("action")

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()

    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)

    quantity = 0
    item_total = 0

    if CartItem.objects.filter(cart=cart, dish=dish).exists():
        updated_item = CartItem.objects.get(cart=cart, dish=dish)
        quantity = updated_item.quantity
        item_total = updated_item.subtotal()

    return JsonResponse({
        "success": True,
        "quantity": quantity,
        "item_total": item_total,
        "cart_count": cart_count,
    })