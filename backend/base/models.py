# In your_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Your MenuItem model is perfect, no changes needed here.
class MenuItem(models.Model):
    CATEGORY_CHOICES = [('food', 'Food'), ('drink', 'Drink')]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='food')
    is_available = models.BooleanField(default=True)
    is_special_today = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

# --- REVISED AND CORRECTED ORDER MODELS ---

class Order(models.Model):
    # If the user is deleted, the order remains (set user to NULL). Good for records.
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Your status field is a great idea!
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note = models.TextField(blank=True) # Your note field is also useful here.

    def __str__(self):
        # We get the username from the user object, which is more reliable.
        return f"Order #{self.id} by {self.user.username if self.user else 'Guest'}"

class OrderItem(models.Model):
    # This is the "line item" on the receipt.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    # Stores the price at the moment of purchase, so it never changes on old receipts.
    price_at_purchase = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order #{self.order.id}"


# The rest of your models are for other features and can remain as they are.
class Note(models.Model):
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='note')

class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField(default=4)

    def __str__(self):
        return f"Table {self.table_number}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    number_of_people = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user.username}'s booking for {self.number_of_people}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"