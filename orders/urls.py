from django.urls import path
from . import views

urlpatterns = [
    path('orders/new/', views.order_new, name='order_new'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orderDetails/<int:pk>/', views.order_details_edit, name='order_details_edit'),
    path('add_order_detail/', views.add_order_detail, name='add_order_detail'),
]
