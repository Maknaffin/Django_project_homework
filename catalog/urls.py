from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import index, auto_info

app_name = CatalogConfig.name

urlpatterns = [
    path('', index, name='index'),
    # path('<int:pk>/catalog_auto/', catalog_auto, name='catalog_auto'),
    path('<int:pk>/auto_info/', auto_info, name='auto_info'),
    # path('/contacts/', contact)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)