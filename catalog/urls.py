from django.contrib import admin
from django.urls import path
from .views import HomeCatalogView, ContactsCatalogView, ProductListView, ProductDetailView


app_name = 'catalog'


urlpatterns = [
    path('', HomeCatalogView.as_view(), name='home'),
    path('contacts/', ContactsCatalogView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
