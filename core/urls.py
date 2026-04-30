"""
Main URL configuration for your project.
This file connects all your apps together.
"""

from django.contrib import admin
from django.urls import path, include

# Needed to serve uploaded images (media) during development
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # Default Django admin (NOT your custom admin panel)
    # URL: /admin/
    path("admin/", admin.site.urls),

    # Accounts app (login, signup, logout, etc.)
    # Root URL → http://127.0.0.1:8000/
    path("", include("accounts.urls")),

    # Customer dashboard and pages
    # URL: /customer/
    path("customer/", include("customer.urls")),

    # Orders system (cart, checkout, orders)
    # URL: /orders/
    path("orders/", include("orders.urls")),

    # Your custom admin panel (IMPORTANT)
    # URL: /admin-panel/
    path("admin-panel/", include("adminpanel.urls")),
]


# Serve uploaded media files (images) in development
# Example: /media/dishes/image.jpg
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)