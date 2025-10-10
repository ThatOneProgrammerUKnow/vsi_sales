from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not getattr(self, "id", False):
            self.created = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True

class BaseGroupModel(BaseModel):
    group = models.ForeignKey("accounts.Group", on_delete=models.CASCADE)

    class Meta:
        abstract = True
