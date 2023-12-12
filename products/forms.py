from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'price',
            'sellingPrice'
        )

class ProductFormEdit(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name',
            'count',
            'price',
            'sellingPrice'
        )