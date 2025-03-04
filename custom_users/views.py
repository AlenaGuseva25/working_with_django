from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_mail(
                'Добро пожаловать!',
                'Спасибо за регистрацию!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Вы успешно зарегистрированы и вошли в систему.")
            return redirect('/catalog/')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=form.cleaned_data.get('username'), password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно вошли в систему.")
                return redirect('/catalog/')
            else:
                messages.error(request, "Неверный email или пароль.")
                return render(request, 'registration/login.html', {'form': form,
                                                                      'error': 'Неверный email или пароль'})
        else:
            messages.error(request, "Неверный email или пароль.")
            return render(request, 'registration/login.html', {'form': form,
                                                                  'error': 'Неверный email или пароль'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('/catalog/')
