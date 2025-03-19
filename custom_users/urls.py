from django.urls import path
from .views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'custom_users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog:product_list'), name='logout'),
]