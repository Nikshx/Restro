from django.db import models
from django.contrib.auth.models import User

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('drink', 'Drink'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price= models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='food')  # 👈 add this
    is_available = models.BooleanField(default=True)
    is_special_today = models.BooleanField(default=False)

    def __str__(self):
        return self.name

 
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed')
    ]

    name = models.CharField(max_length=100) 
    items = models.ManyToManyField(MenuItem)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.name}"
    
class Note(models.Model):
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='note')