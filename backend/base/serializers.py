from rest_framework import serializers

from .unsplash_utils import fetch_unsplash_image
from .models import *
from django.contrib.auth.models import User

class MenuItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'category', 'image_url']

    def get_image_url(self, obj):
        image_url = fetch_unsplash_image(obj.name)
        return image_url or ""

class OrderSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)  
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MenuItem.objects.all(), write_only=True, source='items'  # for POST
    )

    class Meta:
        model = Order
        fields = ['id', 'name', 'items', 'item_ids', 'note', 'status', 'created_at']
        
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'description']
