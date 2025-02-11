import uuid
from django.db import models
from django.contrib.auth.models import User  
from django.core.validators import MinLengthValidator
from django.db.models import Sum

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)  
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def total_orders(self):
        return self.orders.count()

    @property
    def total_spent(self):
        return max(0, self.orders.aggregate(total=Sum('total_amount'))['total'] or 0)

