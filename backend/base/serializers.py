from rest_framework import serializers
from .models import  MenuItem, Order, Note
from django.contrib.auth.models import User

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price']

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
        field=['id','description']