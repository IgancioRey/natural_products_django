from django.urls import path
from . import views

urlpatterns = [
    path('orders/new/', views.order_new, name='order_new'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
