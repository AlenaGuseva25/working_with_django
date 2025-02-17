from django.contrib import admin
from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path("home/", views.home_catalog, name="home"),
    path("contacts/", views.contacts_catalog, name="contacts"),
    path("products/<int:pk>/", views.product_detail, name="product"),
    path("products/", views.product_list, name="product_list"),
]
