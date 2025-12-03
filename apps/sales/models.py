from django.db import models
from apps.shared.base_models import BaseModel
from django.core.exceptions import ValidationError
from datetime import date
from django.utils import timezone 
from phonenumber_field.modelfields import PhoneNumberField
from apps.accounts.models import Company
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator

#=====# Validation #=====#
def valid_sa_vat(value):
    # Accept blank values; when provided, must be exactly 10 digits
    if value and (not value.isdigit() or len(value) != 10):
        raise ValidationError("VAT Number must be 10 digits long") 
#----------------------------------#
#=====# Choices #=====#
class Status(BaseModel):
    status = models.CharField(max_length=100, default="Pending")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.status

#=====# Clients #=====#
class Client(BaseModel):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    vat_number = models.CharField(blank=True, null=True, max_length=20, validators=[valid_sa_vat])
    vat_verified = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.name} {self.surname}"

#=====# Products #=====#
class Product(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    name = models.CharField(max_length=224)
    price_before_vat = models.DecimalField(decimal_places=2, max_digits=12)
    price_after_vat = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):

        # === ID GENERATION ===
        if not self.id:
            # Only pull IDs for NW pattern
            last_product = Product.objects.filter(id__startswith="NW")

            if last_product.exists():
                last_id = last_product.order_by("id").last()
                num = int(last_id.id[2:]) + 1
            else:
                num = 1

            # Auto-evolve format based on size of num
            length = max(2, len(str(num)))
            self.id = f"NW{num:0{length}d}"

        # === VAT CALCULATION ===
        if self.price_before_vat is not None:
            self.price_after_vat = self.price_before_vat * Decimal("1.15")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

#=====# Orders #=====#
class Order(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Get current year and month in yymm format
            now = timezone.now()
            prefix = now.strftime("%y%m")  # e.g. 2511 for Nov 2025

            # Find the last Order with the same prefix (IDs look like OYYMM##)
            last = Order.objects.filter(id__startswith=f"O{prefix}").order_by('-id').first()
            if last:
                # Extract numeric suffix and increment
                num = int(last.id[-2:]) + 1
            else:
                num = 1

            # Format suffix with two digits
            self.id = f"O{prefix}{num:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order number: {self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0), validators=[MinValueValidator(0), MaxValueValidator(100)])
    price_at_checkout = models.DecimalField(max_digits=10, decimal_places=2)


    #=====# Invoice #=====#
class Invoice(BaseModel):
    id = models.CharField(primary_key=True, max_length=10, editable=False)
    date = models.DateField()
    pay_by_date = models.DateField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            # Get current year and month in yymm format
            now = timezone.now()
            prefix = now.strftime("%y%m")  # e.g. 2511 for Nov 2025

            # Find the last record with the same prefix
            last = Invoice.objects.filter(id__startswith=f"I{prefix}").order_by('-id').first()
            if last:
                # Extract numeric suffix and increment
                num = int(last.id[-2:]) + 1
            else:
                num = 1

            # Format suffix with two digits
            self.id = f"I{prefix}{num:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice ID: {self.id}"





    


