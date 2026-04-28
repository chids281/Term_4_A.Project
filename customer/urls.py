from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('payment/', views.payment, name='payment'),
    path('offers/', views.offers, name='offers'),
    path('help-center/', views.help_center, name='help_center'),
    path("category/<int:category_id>/", views.category_dishes, name="category_dishes"),
]