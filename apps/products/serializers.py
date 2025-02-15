from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'currency', 'category', 'tags', 'file_url', 'image_url', 'is_active', 'created_at', 'updated_at']
        
