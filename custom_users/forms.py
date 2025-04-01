from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=False, help_text='Необязательное поле. Введите номер телефона')
    username = forms.CharField(max_length=50, required=False)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')
        return phone

