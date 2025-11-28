import uuid
from django.contrib.auth.models import AbstractUser
from vsi_business.base_models import BaseModel
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

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
