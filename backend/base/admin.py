from django.contrib import admin
from .models import MenuItem, Order, Table, Booking


admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(Table)
admin.site.register(Booking)


