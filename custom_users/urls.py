from multiprocessing.resource_tracker import register

from django.urls import path
from . import views

app_name = 'custom_users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]