from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаление существующих продуктов и категорий, а также добавление тестовых'

    def handle(self, *args, **options):
        """Удаление существующих продуктов и категорий"""
        deleted_products_count, _ = Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено продуктов: {deleted_products_count}'))

        deleted_categories_count, _ = Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено категорий: {deleted_categories_count}'))

        # Создание тестовой категории
        category, _ = Category.objects.get_or_create(name='Тестовая категория')
        self.stdout.write(self.style.SUCCESS(f'Используется категория: {category.name}'))

        # Список тестовых продуктов
        test_products = [
            {'name': 'Test Product 1', 'description': 'Описание продукта 1', 'category': category, 'purchase_price': 100},
            {'name': 'Test Product 2', 'description': 'Описание продукта 2', 'category': category, 'purchase_price': 200},
            {'name': 'Test Product 3', 'description': 'Описание продукта 3', 'category': category, 'purchase_price': 300},
        ]

        # Создание тестовых продуктов
        for product in test_products:
            product_obj, created = Product.objects.get_or_create(
                name=product['name'],
                defaults={
                    'description': product['description'],
                    'category': category,
                    'purchase_price': product['purchase_price']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Добавлен продукт: {product_obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {product_obj.name}'))
