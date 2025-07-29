# In your_app/views.py

from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import models, transaction
from rest_framework import generics, status, permissions, serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
import requests
from django.db.models import Sum
from rest_framework.views import APIView


from .models import MenuItem, Order, OrderItem, Table, Booking
from .serializers import (
    UserSerializer, MyTokenObtainPairSerializer, MenuItemSerializer, 
    OrderSerializer, TableSerializer, BookingSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


class CreateOrderView(generics.CreateAPIView):
    """
    Handles the creation of a new order from the user's cart.
    This is the main endpoint for the checkout process.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer # Uses OrderSerializer for response format

    @transaction.atomic # Ensures all database operations are a single, safe transaction
    def create(self, request, *args, **kwargs):
        # 1. Get the cart data sent from the frontend
        cart_items = request.data.get('cart', [])
        if not cart_items:
            return Response({'error': 'Cart cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Create the main Order object, linked to the current user
        order = Order.objects.create(user=request.user, total_price=0)
        total_order_price = 0

        # 3. Loop through each item in the cart
        for item_data in cart_items:
            try:
                menu_item = MenuItem.objects.get(id=item_data['id'])
                quantity = int(item_data['quantity'])
                price_at_purchase = menu_item.price # Get price from the definitive source
                
                # Create the "line item" for the receipt
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price_at_purchase=price_at_purchase
                )
                # Add this item's subtotal to the grand total
                total_order_price += (price_at_purchase * quantity)
            except MenuItem.DoesNotExist:
                # If any item is invalid, the whole transaction is rolled back
                return Response(
                    {'error': f"Menu item with id {item_data['id']} not found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except (ValueError, TypeError):
                return Response(
                    {'error': 'Invalid quantity provided for an item.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 4. Update the order's final total price and save
        order.total_price = total_order_price
        order.save()

        # 5. Serialize the complete order and return it as a success response
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderRetrieveView(generics.RetrieveAPIView):
    """
    Fetches a single, specific order by its ID.
    Used for the order confirmation/receipt page.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only retrieve their own orders
        return Order.objects.filter(user=self.request.user)

# --- End of New/Corrected Order Views ---


# --- ALL YOUR OTHER VIEWS ARE CORRECT AND REMAIN BELOW ---
class OrderListView(generics.ListAPIView):
    """
    Provides a list of all past orders for the currently authenticated user.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This method is overridden to ensure that users can only see their own orders.
        It filters the Order objects based on the user making the request.
        """
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MenuItemList(generics.ListAPIView): # Changed to ListAPIView as create is handled elsewhere
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny] # Allow guests to see the menu
    queryset = MenuItem.objects.filter(is_available=True)

class TableList(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateBooking(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        table = serializer.validated_data['table']
        people_to_book = serializer.validated_data['number_of_people']
        seats_taken_agg = Booking.objects.filter(table=table).aggregate(total=Sum('number_of_people'))
        seats_taken = seats_taken_agg['total'] or 0
        seats_remaining = table.capacity - seats_taken
        if people_to_book > seats_remaining:
            raise serializers.ValidationError(f"Cannot book {people_to_book} seats. Only {seats_remaining} available.")
        serializer.save()

