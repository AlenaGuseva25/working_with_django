from django.views.decorators.cache import cache_page

from . import views
from django.urls import path
from catalog.views import (
    HomeCatalogView,
    ContactsCatalogView,
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductUnpublishView,
    ProductByCategoryView,
)


app_name = 'catalog'

urlpatterns = [
    path('', HomeCatalogView.as_view(), name='home'),
    path('contacts/', ContactsCatalogView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', cache_page(60 * 5)(views.ProductDetailView.as_view()), name='product'),
    path('product/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('products_list/', ProductListView.as_view(), name='product_list'),
    path('category/<str:category_name>/', ProductByCategoryView.as_view(), name='products_by_category'),

]
