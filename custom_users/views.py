from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import RegisterForm
from django.core.mail import send_mail
from django.conf import settings
from .models import User

from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать'
        message = 'Спасибо за регистрацию!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)