from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import PermissionsMixin

from custom_users.models import User
from .models import Product

FORBIDDEN_WORDS = [
    'криптовалюта',
    'казино',
    'крипта',
    'дешево',
    'бесплатно',
    'биржа',
    'обман',
    'полиция',
    'радар',
]


class ProductForm(forms.ModelForm):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput,label='Оставить пустым')
    class Meta:
        model = Product
        fields = ['name', 'description', 'purchase_price', 'category', 'image', 'is_published']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_honeypot(self):
        value = self.cleaned_data.get('honeypot')
        if value:
            raise forms.ValidationError('СПАМ')
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name')
        self.validate_forbidden_words(name)
        return name


    def clean_description(self):
        description = self.cleaned_data.get('description')
        self.validate_forbidden_words(description)
        return description


    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if purchase_price is None:
            raise forms.ValidationError('Цена не может быть пустой')
        if purchase_price <= 0:
            raise forms.ValidationError('Цена не должна быть отрицательной или равной 0')
        return purchase_price



    def validate_forbidden_words(self, value):
        if value:
            value_lower = value.lower()
            for word in FORBIDDEN_WORDS:
                if word in value_lower:
                    raise forms.ValidationError(f'Слово "{word}" недопустимо')

