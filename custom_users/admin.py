from django.contrib import admin

from custom_users.models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ['email']
    search_fields = ('username', 'email', 'first_name', 'last_name')

