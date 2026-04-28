from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path("dish/<int:dish_id>/", views.dish_detail, name="dish_detail"),
    path('update-dish-cart/<int:dish_id>/', views.update_dish_cart, name='update_dish_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path("delete/<int:order_id>/", views.delete_order, name="delete_order"),
    path("live-status/<int:order_id>/", views.live_order_status, name="live_order_status"),
]