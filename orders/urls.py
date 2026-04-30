# Import path for URL routing
from django.urls import path

# Import views from this app
from . import views


# Add namespace (VERY IMPORTANT to avoid NoReverseMatch errors)
app_name = "orders"


urlpatterns = [

    # =====================
    # CART
    # =====================

    # View cart page
    # URL: /orders/cart/
    path('cart/', views.cart_view, name='cart'),

    # Add a dish to cart
    # URL: /orders/add-to-cart/5/
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),

    # Remove item from cart
    # URL: /orders/remove-from-cart/3/
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Update quantity (+ / - buttons)
    # URL: /orders/update-cart/3/
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),

    # =====================
    # DISH DETAIL (with cart interaction)
    # =====================

    # View single dish details
    # URL: /orders/dish/5/
    path("dish/<int:dish_id>/", views.dish_detail, name="dish_detail"),

    # Update cart directly from dish page
    path('update-dish-cart/<int:dish_id>/', views.update_dish_cart, name='update_dish_cart'),

    # =====================
    # CHECKOUT & ORDER
    # =====================

    # Checkout page
    path('checkout/', views.checkout_view, name='checkout'),

    # Order success page (after placing order)
    path('order-success/', views.order_success, name='order_success'),

    # =====================
    # USER ORDERS
    # =====================

    # View all user orders
    path('my-orders/', views.my_orders, name='my_orders'),

    # Delete/cancel an order
    path("delete/<int:order_id>/", views.delete_order, name="delete_order"),

    # Live order tracking (your animation page 👀🔥)
    path("live-status/<int:order_id>/", views.live_order_status, name="live_order_status"),
]