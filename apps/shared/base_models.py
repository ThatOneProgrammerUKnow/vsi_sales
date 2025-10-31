from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    # Prefer setting these timestamps in the save() method rather than using `auto_now` and `auto_now_add`
    # See https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not getattr(self, "id", False):
            self.created = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
