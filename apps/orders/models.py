from django.db import models
import uuid
from apps.products.models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError
import random
from datetime import datetime

def generate_order_number():
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

def validate_quantity(value):
    if value < 1:
        raise ValidationError("Quantity must be at least 1.")

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        'customers.Customer',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    order_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.customer.name}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.IntegerField(validators=[validate_quantity])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order {self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
