from django.shortcuts import render, redirect # type: ignore
from django.contrib.auth import login, logout # type: ignore
from .forms import SignUpForm, LoginForm


def splash_view(request):
    return render(request, 'accounts/splash.html')


def onboarding_view(request):
    return render(request, 'accounts/onboarding.html')


def auth_choice_view(request):
    return render(request, 'accounts/auth_choice.html')


def redirect_user_by_role(user):
    if user.role == 'customer':
        return redirect('customer_dashboard')
    elif user.role == 'owner':
        return redirect('owner_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    return redirect('auth_choice')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_by_role(user)
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_by_role(user)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')