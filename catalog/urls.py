from django.contrib import admin
from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", views.home_catalog, name="home"),
    path("contacts/", views.contacts_catalog, name="contacts"),
]
