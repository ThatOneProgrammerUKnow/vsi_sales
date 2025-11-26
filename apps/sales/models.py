from django.db import models
from apps.shared.base_models import BaseModel
from datetime import date
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

#=====# Clients #=====#
class Client(BaseModel):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    email = models.EmailField()

#=====# Products #=====#
class Product(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    name = models.CharField(max_length = 224)
    price = models.DecimalField(decimal_places=2, max_digits=12)

    def save(self, *args, **kwargs):
        if not self.id:
            # Get the last inserted ID
            last_id = Product.objects.order_by('-id').first()
            if last_id:
                # Extract the numeric part and increment
                num = int(last_id.id[2:]) + 1
            else:
                num = 1
            # Format as HH01, HH02, etc.
            self.id = f"HH{num:02d}"
        super().save(*args, **kwargs)

#=====# Invoice #=====#
class Invoice(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    date = models.DateField()
    pay_by_date = models.DateField()
    products = models.ManyToManyField(Product)


    def save(self, *args, **kwargs):
        if not self.id:
            # Get current year and month in yymm format
            now = timezone.now()
            prefix = now.strftime("%y%m")  # e.g. 2511 for Nov 2025

            # Find the last record with the same prefix
            last = Invoice.objects.filter(id__startswith=prefix).order_by('-id').first()
            if last:
                # Extract numeric suffix and increment
                num = int(last.id[-2:]) + 1
            else:
                num = 1

            # Format suffix with two digits
            self.id = f"{prefix}{num:02d}"

        super().save(*args, **kwargs)

    


