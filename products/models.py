from django.db import models
from django.utils import timezone
from datetime import date


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
    createdDate = models.DateField()
    lastModifiedDate = models.DateField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.createdDate:
            self.createdDate = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_data(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'count': self.count,
            'price': float(str(self.price)),
            'sellingPrice': float(str(self.sellingPrice)),
            'createdDate': self.createdDate,
            'lastModifiedDate': self.lastModifiedDate
        }
