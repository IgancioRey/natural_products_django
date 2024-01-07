from django.db import models
from django.utils import timezone


# Create your models here.
class Customer(models.Model):
    firstName = models.CharField(
        max_length=20,
        default='',
        blank=False,
        null=False
    )
    lastName = models.CharField(
        max_length=15,
        default='',
        blank=False,
        null=False
    )
    mobileNumber = models.CharField(
        max_length=12,
        default=None,
        null=True
    )
    observation = models.CharField(
        max_length=255,
        default=None,
        null=True
    )
    createdDate = models.DateField()
    lastModifiedDate = models.DateField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.createdDate:
            self.createdDate = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.firstName + ' ' + self.lastName

    def get_data(self):
        return {
            'pk': self.pk,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'mobileNumber': self.mobileNumber,
            'observation': self.observation,
            'createdDate': self.createdDate,
            'lastModifiedDate': self.lastModifiedDate
        }
