from django.db import models
from django.conf import settings


# ======================
# CATEGORY
# ======================
class Category(models.Model):
    # Name of the category (e.g., Pizza, Drinks, Burgers)
    name = models.CharField(max_length=100)

    def __str__(self):
        # What shows in admin panel / shell
        return self.name


# ======================
# RESTAURANT
# ======================
class Restaurant(models.Model):
    # Restaurant name
    name = models.CharField(max_length=150)

    # Owner of the restaurant (must be a user with role = owner ideally)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Restaurant address
    address = models.TextField(blank=True)

    # Optional image/logo of restaurant
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)

    def __str__(self):
        return self.name


# ======================
# DISH
# ======================
class Dish(models.Model):
    # Name of the dish (e.g., Chicken Burger)
    name = models.CharField(max_length=100)

    # Price of the dish
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Dish image (stored in media/dishes/)
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)

    # Category (can be null if not assigned yet)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Restaurant that owns this dish
    # TEMPORARY nullable (used to fix migration issues earlier)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name