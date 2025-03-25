from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создание группы Модератор продуктов'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        can_unpublish_product = Permission.objects.get(
            codename='can_unpublish_product',
            content_type__app_label='catalog',
            content_type__model='product'
        )

        group.permissions.add(can_unpublish_product)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана и права назначены.'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует.'))


