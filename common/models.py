from django.db import models


class CustomTimeStamp(models.Model):
    """ Custom abstract class to store timestamps """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True