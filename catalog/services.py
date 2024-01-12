from django.conf import settings
from django.core.cache import cache

from .models import Product


def get_cached_objects_for_products():
    if settings.CACHE_ENABLED:
        key = f'object_list'
        object_list = cache.get(key)
        if object_list is None:
            object_list = Product.objects.all()
            cache.set(key, object_list)
    else:
        object_list = Product.objects.all()
    return object_list