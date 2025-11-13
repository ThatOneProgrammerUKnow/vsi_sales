from django.contrib import admin
from .models import Customer, ContactPerson, GRN, GoodsItem 

# Register your models here.
admin.site.register(Customer)
admin.site.register(ContactPerson)
admin.site.register(GRN)
admin.site.register(GoodsItem)