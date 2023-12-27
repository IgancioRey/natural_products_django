from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list, name='products_list'),
    path('products/data/', views.product_list_json, name='products_list_json'),
    path('products/new/', views.product_new, name='product_new'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/edit_modal/', views.product_edit_modal, name='product_edit_modal'),
]
