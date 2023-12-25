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


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='Slug', **NULLABLE)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение (превью)')
    date_of_creation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'

class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    num_version = models.IntegerField(verbose_name='Номер версии')
    name_version = models.CharField(max_length=150, verbose_name='Название версии')
    is_active = models.BooleanField(default=True, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.name_version} ({self.num_version})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'