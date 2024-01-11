from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from catalog.apps import CatalogConfig
from catalog.views import IndexView, ProductCreateView, ProductUpdateView, BlogCreateView, \
    BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', cache_page(60)(IndexView.as_view()), name='index'),
    # path('auto_info/<int:pk>/', auto_info, name='auto_info'),
    path('auto_info/<int:pk>/', cache_page(60)(ProductListView.as_view()), name='auto_info'),
    path('create/', never_cache(ProductCreateView.as_view()), name='product_create'),
    path('update/<int:pk>/', never_cache(ProductUpdateView.as_view()), name='product_update'),

    path('create/', never_cache(BlogCreateView.as_view()), name='blog_create'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='blog_edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)