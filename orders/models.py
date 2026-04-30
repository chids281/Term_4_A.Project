from django.db import models
from django.conf import settings
from restaurant.models import Dish


# =========================
# CART
# =========================

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"


# =========================
# ORDER
# =========================

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("on_the_way", "On the way"),
        ("delivered", "Delivered"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Customer Info
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    payment_method = models.CharField(max_length=20)
    is_paid = models.BooleanField(default=False)

    # Status Tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Timestamps (VERY IMPORTANT for tracking UI)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    preparing_at = models.DateTimeField(null=True, blank=True)
    on_the_way_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def progress_percentage(self):
        mapping = {
            "pending": 10,
            "confirmed": 25,
            "preparing": 50,
            "on_the_way": 75,
            "delivered": 100,
        }
        return mapping.get(self.status, 0)


# =========================
# ORDER ITEMS
# =========================

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"