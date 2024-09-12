from django.db import models

class ActiveObjectsManager(models.Manager):
    """Active Objects manager."""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)