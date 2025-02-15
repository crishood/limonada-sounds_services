from django.db import models
import uuid

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Drum Kit', 'Drum Kit'),
        ('Presets', 'Presets'),
        ('Effects Rack', 'Effects Rack'),
        ('MIDI Rack', 'MIDI Rack'),
        ('Samples', 'Samples'),
        ('VST', 'VST'),
        ('Max4Live Patch', 'Max4Live Patch'),
        ('Max4Live Device', 'Max4Live Device'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    tags = models.JSONField(default=list, blank=True, null=True)
    file_url = models.TextField()
    image_url = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
