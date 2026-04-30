# Import Django's path function to define URL routes
from django.urls import path

# Import all views from the current app
from . import views


# This defines a namespace for this app
# It allows you to reference URLs like: adminpanel:dashboard in templates
app_name = 'adminpanel'


# List of all URL patterns for the admin panel
urlpatterns = [

    # Dashboard page (main admin landing page)
    # URL: /adminpanel/
    path('', views.dashboard, name='dashboard'),

    # Categories management page
    # Displays all categories and possibly allows adding/editing
    # URL: /adminpanel/categories/
    path('categories/', views.categories, name='categories'),

    # Delete a specific category using its primary key (id)
    # <int:pk> captures the category ID from the URL
    # Example: /adminpanel/categories/delete/5/
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Food types page (e.g., Veg, Non-Veg, Drinks, etc.)
    # URL: /adminpanel/food-types/
    path('food-types/', views.food_types, name='food_types'),

    # Reports page (could show analytics like orders, revenue, etc.)
    # URL: /adminpanel/reports/
    path('reports/', views.reports, name='reports'),

    # Orders management page for admin
    # Shows all customer orders and their statuses
    # URL: /adminpanel/orders/
    path('orders/', views.orders, name='orders'),

    # Admin profile page
    # Allows admin to view/edit personal details
    # URL: /adminpanel/profile/
    path('profile/', views.profile, name='profile'),
]