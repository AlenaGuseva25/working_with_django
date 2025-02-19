from django.db import models


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name






class Category(models.Model):
    """Модель Категория с базовыми настройками"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    description = models.TextField(verbose_name='Описание категории')


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']


    def __str__(self):
        return f'{self.name} {self.description}'


class Product(models.Model):
    """Модель Продукт с базовыми настройками"""
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    description = models.TextField(null=True, blank=True, verbose_name='Описание продукта')
    image = models.ImageField(upload_to='photos/', verbose_name='Изображение продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name']


    def __str__(self):
        return (f'{self.name} {self.description} {self.purchase_price} {self.category} {self.created_at} {self.updated_at}')




