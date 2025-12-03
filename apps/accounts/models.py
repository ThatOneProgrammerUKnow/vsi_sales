import uuid
from django.contrib.auth.models import AbstractUser
from vsi_business.base_models import BaseModel
from django.db import models

#====================================# Plan #====================================#
class Plan(BaseModel):
    name = models.CharField(max_length=50)
    max_orders_per_week = models.IntegerField(null = True, blank=True)
    max_user = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def __str__(self):
        return f"{self.name} - R {self.price}"

#====================================#  Company #====================================#
class Company(BaseModel):
    name = models.CharField(max_length=255)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    subscription_expires_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
 
#====================================# Adress #====================================#
class Address(BaseModel):
    street = models.CharField(max_length=50, blank=True, null=True)  # street number + name
    unit = models.CharField(max_length=50, blank=True, null=True)  # optional apartment/unit
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, default="South Africa")
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


    def __str__(self):
        unit = ""
        address = f"{unit}{self.street}, {self.city}, {self.province}, {self.country}"
        if self.unit:
            unit = f"{self.unit}, "
        return address
#====================================# Banking Details #====================================#
class BankDetails(models.Model):
    company = models.OneToOneField('Company', on_delete=models.CASCADE, related_name='bank_details')
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    branch_name = models.CharField(max_length=100, blank=True, null=True)
    branch_code = models.CharField(max_length=20, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"


#====================================# Custom User #====================================#
class User(AbstractUser):
    REQUIRED_ACCOUNT_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "password",
    ]

    identification_number = models.CharField(max_length=13, blank=True, null=True)
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    email = models.EmailField("email address", unique=True)

    # Other
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
