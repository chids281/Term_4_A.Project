from django.db import models
from django.conf import settings
from restaurant.models import Dish


# =========================
# CART
# =========================

class Cart(models.Model):
    # Each user has ONLY one cart
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        # Helps identify the cart in admin panel
        return f"{self.user.username}'s Cart"

    def total_price(self):
        # Sum of all cart item subtotals
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    # Each cart can have multiple items
    # related_name="items" allows: cart.items.all()
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # The food item added to cart
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    # Quantity of the dish
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        # Price for this specific item
        return self.dish.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"


# =========================
# ORDER
# =========================

class Order(models.Model):

    # All possible order statuses (used for tracking UI)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("on_the_way", "On the way"),
        ("delivered", "Delivered"),
    ]

    # The user who placed the order
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Customer Info (saved at time of order)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    note = models.TextField(blank=True, null=True)

    # Pricing details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment info
    payment_method = models.CharField(max_length=20)
    is_paid = models.BooleanField(default=False)

    # Order status (used for progress tracking)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # Timestamps for each stage (used for timeline UI)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    preparing_at = models.DateTimeField(null=True, blank=True)
    on_the_way_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def progress_percentage(self):
        # Used for progress bar animation
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
    # Each order can have multiple items
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

    # Dish at the time of purchase
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    # Quantity ordered
    quantity = models.PositiveIntegerField()

    # Store price at time of purchase (VERY IMPORTANT)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        # Total price for this item
        return self.price * self.quantity

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"