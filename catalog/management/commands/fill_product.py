from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        Product.objects.all().delete()

        product_list = [
            {
                'pk': 1,
                'name': 'Яблоко',
                'price_for_one': '70',
                'category': Category.objects.get(pk=1)
            },
            {
                'pk': 2,
                'name': 'Груша',
                'price_for_one': '65',
                'category': Category.objects.get(pk=1)
            },
            {
                'pk': 3,
                'name': 'Гранат',
                'price_for_one': '90',
                'category': Category.objects.get(pk=1)
            },
            {
                'pk': 4,
                'name': 'Морковь',
                'price_for_one': '60',
                'category': Category.objects.get(pk=2)
            },
            {
                'pk': 5,
                'name': 'Картофель',
                'price_for_one': '50',
                'category': Category.objects.get(pk=2)
            },
            {
                'pk': 6,
                'name': 'Лук',
                'price_for_one': '55',
                'category': Category.objects.get(pk=2)
            },
        ]

        product_for_create = []
        for product_item in product_list:
            product_for_create.append(Product(**product_item))
        Product.objects.bulk_create(product_for_create)
