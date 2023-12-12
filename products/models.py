from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        default='',
        blank=False,
        null=False
    )
    count = models.IntegerField(
        default=0,
        blank=False,
        null=False
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default='',
        blank=False,
        null=False
    )
    sellingPrice = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default='',
        blank=False,
        null=False
    )
    createdDate = models.DateField(
        default=timezone.now()
    )
    lastModifiedDate = models.DateField(
        blank=True, 
        null=True
    )
