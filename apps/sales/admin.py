from django.contrib import admin
from .models import Client, Product, Invoice, Order, OrderItem

# Register your models here.
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Order)
admin.site.register(OrderItem)