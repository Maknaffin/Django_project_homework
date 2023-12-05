from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    price_for_one = models.IntegerField(verbose_name='Цена за штуку')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='Наименование')
    descriptions = models.TextField(**NULLABLE, verbose_name='Описание')
    # created_at = models.CharField(max_length=250, verbose_name='Создан в')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
