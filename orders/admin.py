from django.contrib import admin
from orders.models import OrderDetail, Order

admin.site.register(Order)
admin.site.register(OrderDetail)