# Generated by Django 4.2.7 on 2024-01-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_remove_product_manufacturer_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='Признак публикации'),
        ),
    ]
