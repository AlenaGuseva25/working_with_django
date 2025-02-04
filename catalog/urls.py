from django.urls import path
from . import views

app_name = 'catalog'


urlpatterns = [
    path("", views.home_catalog, name="home"),
    path("contacts/", views.contacts_catalog, name="contacts"),
  ]
