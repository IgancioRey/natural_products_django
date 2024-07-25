from decimal import Decimal
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import timezone
from customers.models import Customer
from products.models import Product


# Create your models here.
class Order(models.Model):
    orderDate = models.DateField()
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    paidAmount = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        null=False
    )
    paid = models.BooleanField(default=False)
    withdrawn = models.BooleanField(default=False)
    createdDate = models.DateField()
    lastModifiedDate = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return f"Orden {self.pk} - {self.customer}"

    def get_data(self):
        customer = get_object_or_404(Customer, pk=self.customer)
        return {
            'pk': self.pk,
            'orderDate': self.orderDate,
            'customer': customer,
            'paidAmount': float(str(self.paidAmount)),
            'paid': self.paid,
            'withdrawn': self.withdrawn,
            'createdDate': self.createdDate,
            'lastModifiedDate': self.lastModifiedDate
        }

    def save(self, *args, **kwargs):
        if not self.createdDate:
            self.createdDate = timezone.now().date()
        super().save(*args, **kwargs)


class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    count = models.PositiveIntegerField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Producto: {self.pk} - {self.product.name} - Cantidad: {self.count}"
    
    @property
    def subTotal(self):
        return Decimal(self.count) * Decimal(str(self.amount))
    
    def get_data(self):
        order = get_object_or_404(Order, pk=self.order)
        product = get_object_or_404(Product, pk=self.product)
        return {
            'pk': self.pk,
            'order': order,
            'product': product,
            'count': self.count,
            'amount': self.amount,
            'subTotal': self.subTotal,
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = self.product
        product.count += self.count
        product.save()
