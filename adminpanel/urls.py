from django.urls import path
from . import views
 
app_name = 'adminpanel'
 
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('food-types/', views.food_types, name='food_types'),
    path('reports/', views.reports, name='reports'),
    path('orders/', views.orders, name='orders'),
    path('profile/', views.profile, name='profile'),
]