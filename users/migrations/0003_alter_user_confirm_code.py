# Generated by Django 5.0.1 on 2024-03-13 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirm_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirm_code',
            field=models.CharField(blank=True, default='33254059', max_length=8, null=True, verbose_name='Код подтверждения'),
        ),
    ]
