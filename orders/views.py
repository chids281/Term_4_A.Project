# Import tools for rendering pages, redirecting users, and safely fetching objects
from django.shortcuts import render, redirect, get_object_or_404

# Ensures only logged-in users can access these views
from django.contrib.auth.decorators import login_required

# Restricts a view to only accept POST requests
from django.views.decorators.http import require_POST

# Used to return JSON responses for AJAX/fetch requests
from django.http import JsonResponse

# Used for time-based order tracking
from django.utils import timezone
from datetime import timedelta

# Import models
from restaurant.models import Dish
from .models import Cart, CartItem, Order, OrderItem


# Fixed delivery fee for every order
DELIVERY_FEE = 1000


# Helper function to calculate cart totals in one place
def get_cart_totals(cart):
    cart_items = CartItem.objects.filter(cart=cart)

    # Total price of all cart items before delivery fee
    subtotal = sum(item.subtotal() for item in cart_items)

    # Add delivery fee only if cart is not empty
    total = subtotal + DELIVERY_FEE if subtotal > 0 else 0

    # Total number of items in the cart
    cart_count = sum(item.quantity for item in cart_items)

    return cart_items, subtotal, total, cart_count


# =====================
# CART PAGE
# =====================
@login_required
def cart_view(request):
    # Get the user's cart or create one if it does not exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Calculate cart totals
    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    return render(request, 'orders/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'delivery_fee': DELIVERY_FEE,
        'total': total,
        'cart_count': cart_count,
    })


# =====================
# ADD TO CART
# =====================
@login_required
def add_to_cart(request, dish_id):
    # Get selected dish or return 404 if it does not exist
    dish = get_object_or_404(Dish, id=dish_id)

    # Get or create cart for current user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get cart item if dish already exists in cart, otherwise create it
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    # If item already exists, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Recalculate cart count after adding item
    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    # If request came from AJAX, return JSON instead of redirecting
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "cart_count": cart_count,
            "message": f"{dish.name} added to cart",
        })

    return redirect("orders:cart")


# =====================
# REMOVE FROM CART
# =====================
@login_required
def remove_from_cart(request, item_id):
    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get cart item that belongs to this user's cart
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    # Delete the item
    item.delete()

    # Recalculate totals
    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    # Return updated values for AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "removed": True,
            "subtotal": subtotal,
            "total": total,
            "cart_count": cart_count,
        })

    return redirect("orders:cart")


# =====================
# UPDATE CART QUANTITY
# =====================
@require_POST
@login_required
def update_cart(request, item_id):
    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get the cart item being updated
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart
    )

    # Get button action: increase or decrease
    action = request.POST.get("action")
    removed = False

    if action == "increase":
        item.quantity += 1
        item.save()

    elif action == "decrease":
        # Reduce quantity if more than 1
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            # Remove item completely if quantity becomes 0
            item.delete()
            removed = True

    else:
        return JsonResponse({
            "success": False,
            "error": "Invalid action"
        }, status=400)

    # Recalculate totals after update
    cart_items, subtotal, total, cart_count = get_cart_totals(cart)

    # Return JSON for AJAX update
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

    return redirect("orders:cart")


# =====================
# DISH DETAIL PAGE
# =====================
@login_required
def dish_detail(request, dish_id):
    # Get selected dish
    dish = get_object_or_404(Dish, id=dish_id)

    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if this dish is already in cart
    cart_item = CartItem.objects.filter(cart=cart, dish=dish).first()

    # Count all cart items for navbar badge
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)

    return render(request, "orders/dish_detail.html", {
        "dish": dish,
        "cart_item": cart_item,
        "cart_count": cart_count,
    })


# =====================
# UPDATE CART FROM DISH DETAIL PAGE
# =====================
@login_required
def update_dish_cart(request, dish_id):
    # Get selected dish
    dish = get_object_or_404(Dish, id=dish_id)

    # Get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create cart item for this dish
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        dish=dish
    )

    # Get action from form/AJAX
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

    # Recalculate cart count
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = sum(item.quantity for item in cart_items)

    # Default values if item was deleted
    quantity = 0
    item_total = 0

    # If item still exists, get updated quantity and subtotal
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


# =====================
# CHECKOUT PAGE
# =====================
@login_required
def checkout_view(request):
    # Get user's cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get all cart items
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate totals
    subtotal = sum(item.subtotal() for item in cart_items)
    delivery_fee = DELIVERY_FEE
    total = subtotal + delivery_fee if subtotal > 0 else 0

    # Handle checkout form submission
    if request.method == "POST":

        # Prevent placing an order with an empty cart
        if not cart_items.exists():
            return redirect("orders:cart")

        # Get customer details from checkout form
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        note = request.POST.get("note")
        payment_method = request.POST.get("payment_method")

        # Create the order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            note=note,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            payment_method=payment_method,
        )

        # Copy cart items into order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                dish=item.dish,
                quantity=item.quantity,
                price=item.dish.price
            )

        # Clear cart after successful order
        cart_items.delete()

        # Return JSON if checkout was submitted using AJAX
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "message": "Order placed successfully!"
            })

        return redirect("orders:order_success")

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
    })


# =====================
# ORDER SUCCESS PAGE
# =====================
@login_required
def order_success(request):
    return render(request, "orders/order_success.html")


# =====================
# MY ORDERS PAGE
# =====================
@login_required
def my_orders(request):
    # Get current user's orders, newest first
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    # Update each order status based on time passed
    for order in orders:
        update_order_status(order)

    return render(request, "orders/my_orders.html", {
        "orders": orders
    })


# =====================
# DELETE / CANCEL ORDER
# =====================
@login_required
def delete_order(request, order_id):
    # Only allow user to delete their own order
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Only delete order when form sends POST request
    if request.method == "POST":
        order.delete()

    return redirect("orders:my_orders")


# =====================
# AUTO UPDATE ORDER STATUS
# =====================
def update_order_status(order):
    # Check how long ago the order was created
    time_passed = timezone.now() - order.created_at

    # Move order through stages based on time passed
    if time_passed >= timedelta(minutes=10):
        order.status = "delivered"
    elif time_passed >= timedelta(minutes=6):
        order.status = "on_the_way"
    elif time_passed >= timedelta(minutes=3):
        order.status = "preparing"
    else:
        order.status = "confirmed"

    # Save the new status
    order.save()


# =====================
# LIVE ORDER STATUS API
# =====================
@login_required
def live_order_status(request, order_id):
    # Get order belonging to the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Update status before returning it
    update_order_status(order)

    # Return status as JSON for live tracking UI
    return JsonResponse({
        "status": order.status,
        "status_display": order.get_status_display(),
    })