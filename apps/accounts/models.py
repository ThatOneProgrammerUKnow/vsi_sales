import uuid
from django.contrib.auth.models import AbstractUser
from weg_solutions.base_models import BaseModel, BaseGroupModel
from django.db import models


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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)


class Group(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True, db_index=True)


class GroupUser(BaseGroupModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey("accounts.Group", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "group")
