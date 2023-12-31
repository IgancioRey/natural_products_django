from django.urls import path
from . import views

urlpatterns = [
    path('customers/', views.customers_list, name='customer_list'),
    path('customers/data/', views.customer_list_json, name='customer_list_json'),
    path('customers/<int:pk>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customers/new/', views.customer_new, name='customer_new'),
    path('customers/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
]
