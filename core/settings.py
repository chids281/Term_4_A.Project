"""
Django settings for core project.

This file controls how your Django project behaves:
- apps
- database
- authentication
- static/media files
"""

from pathlib import Path

# BASE_DIR = root folder of your project (Term_4_A.Project)
# Used to build paths for templates, static, media, database, etc.
BASE_DIR = Path(__file__).resolve().parent.parent


# =====================
# SECURITY SETTINGS
# =====================

# Secret key used for cryptographic signing (sessions, tokens, etc.)
# ⚠️ NEVER expose this in production
SECRET_KEY = 'django-insecure-...'

# Debug mode (shows detailed errors)
# ✅ True for development
# ❌ Must be False in production
DEBUG = True

# List of allowed domains (empty = only localhost allowed)
ALLOWED_HOSTS = []


# =====================
# INSTALLED APPS
# =====================

INSTALLED_APPS = [
    # Default Django apps (authentication, admin, sessions, etc.)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Your custom apps (QuickBite)
    'accounts',      # handles login/signup & custom user model
    'restaurant',    # restaurants, categories, dishes
    'orders',        # cart, orders
    'customer',      # customer dashboard/pages
    'adminpanel',    # your custom admin dashboard (NOT Django admin)
]


# =====================
# MIDDLEWARE
# =====================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',   # security features
    'django.contrib.sessions.middleware.SessionMiddleware',  # session handling
    'django.middleware.common.CommonMiddleware',       # general request/response handling
    'django.middleware.csrf.CsrfViewMiddleware',       # CSRF protection (forms)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # user authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # security against clickjacking
]


# Root URL configuration file
ROOT_URLCONF = 'core.urls'


# =====================
# TEMPLATES
# =====================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Global templates folder (important for shared layouts)
        'DIRS': [BASE_DIR / 'templates'],

        # Allows templates inside each app folder
        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # gives access to request in templates
                'django.contrib.auth.context_processors.auth', # gives user object
                'django.contrib.messages.context_processors.messages', # messages support
            ],
        },
    },
]


# WSGI config (used for deployment, not needed for now)
WSGI_APPLICATION = 'core.wsgi.application'


# =====================
# DATABASE
# =====================

DATABASES = {
    'default': {
        # SQLite database (simple, file-based)
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =====================
# PASSWORD VALIDATION
# =====================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        # prevents passwords similar to username/email
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # enforces minimum length
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        # blocks common passwords (e.g., "123456")
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        # blocks fully numeric passwords
    },
]


# =====================
# INTERNATIONAL SETTINGS
# =====================

LANGUAGE_CODE = 'en-us'

# ⚠️ You might want to change this to your local timezone:
# TIME_ZONE = 'Africa/Lagos'
TIME_ZONE = 'UTC'

USE_I18N = True  # translation support
USE_TZ = True    # timezone-aware datetimes


# =====================
# STATIC FILES (CSS, JS)
# =====================

STATIC_URL = '/static/'

# Where Django will look for your static files during development
STATICFILES_DIRS = [BASE_DIR / 'static']


# =====================
# CUSTOM USER MODEL
# =====================

# You are using a custom user model from accounts app
AUTH_USER_MODEL = 'accounts.CustomUser'


# =====================
# MEDIA FILES (uploads)
# =====================

# URL to access uploaded files
MEDIA_URL = '/media/'

# Folder where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'


# =====================
# AUTHENTICATION REDIRECTS
# =====================

# If user tries to access protected page → redirect here
LOGIN_URL = '/login/'

# After login → redirect here
# ⚠️ Make sure this matches your URL config
LOGIN_REDIRECT_URL = '/admin-panel/'