# In your_app/serializers.py

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum
from django.contrib.auth.models import User

# Import all your models
from .models import MenuItem, Order, OrderItem, Note, Table, Booking
from .unsplash_utils import fetch_unsplash_image


class MenuItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'description', 'category', 'image_url']

    def get_image_url(self, obj):
        # This part is fine, assuming your utility function works.
        image_url = fetch_unsplash_image(obj.name)
        return image_url or ""


# --- REVISED AND CORRECTED ORDER SERIALIZERS ---

class OrderItemSerializer(serializers.ModelSerializer):
    # This nested serializer shows the full details of the menu item in the receipt.
    # It's read_only because we create OrderItems based on IDs, not nested data.
    menu_item = MenuItemSerializer(read_only=True) 
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    # This nested serializer will now correctly display the list of OrderItems.
    # The `related_name='items'` in models.py is what allows this to work.
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        # The fields now reflect the new, correct Order model structure.
        fields = ['id', 'user', 'created_at', 'total_price', 'status', 'note', 'items']

# --- END OF REVISED SECTION ---


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'description']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class TableSerializer(serializers.ModelSerializer):
    seats_taken = serializers.SerializerMethodField()
    seats_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'seats_taken', 'seats_remaining']

    def get_seats_taken(self, table_obj):
        result = Booking.objects.filter(table=table_obj).aggregate(total=Sum('number_of_people'))
        return result['total'] or 0

    def get_seats_remaining(self, table_obj):
        seats_taken = self.get_seats_taken(table_obj)
        return table_obj.capacity - seats_taken


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'table', 'number_of_people', 'booking_time']