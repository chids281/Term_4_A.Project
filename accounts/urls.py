from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.splash_view, name='splash'),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('auth/', views.auth_choice_view, name='auth_choice'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]