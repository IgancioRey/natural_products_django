from django import forms
from customers.models import Customer

from orders.models import Order, OrderDetail


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'orderDate',
            'paidAmount',
            'paid',
            'withdrawn'
        )
    paidAmount = forms.DecimalField(required=False)
    paid = forms.BooleanField(required=False)
    withdrawn = forms.BooleanField(required=False)
    customer = forms.IntegerField(required=True)

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = (
            'order',
            'product',
            'count',
            'amount'
        )
