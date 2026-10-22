from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    stock = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [("PLACED", "Placed"), ("PROCESSING", "Processing"), ("SHIPPED", "Shipped")]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shop_orders")
    full_name = models.CharField(max_length=120)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLACED")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
