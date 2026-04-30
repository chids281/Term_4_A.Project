# Import Django's path function to define URL routes
from django.urls import path  # type: ignore

# Import views from this app
from . import views


# URL patterns for the customer app
urlpatterns = [

    # Customer dashboard (main landing page after login)
    # URL: /customer/dashboard/
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),

    # Customer profile page
    # URL: /customer/profile/
    path('profile/', views.profile, name='profile'),

    # Customer orders page (list of past/current orders)
    # URL: /customer/orders/
    path('orders/', views.orders, name='orders'),

    # Payment page
    # URL: /customer/payment/
    path('payment/', views.payment, name='payment'),

    # Offers / promotions page
    # URL: /customer/offers/
    path('offers/', views.offers, name='offers'),

    # Help center / support page
    # URL: /customer/help-center/
    path('help-center/', views.help_center, name='help_center'),

    # Show all dishes in a selected category
    # <int:category_id> captures the category ID from the URL
    # Example: /customer/category/3/
    path("category/<int:category_id>/", views.category_dishes, name="category_dishes"),
]