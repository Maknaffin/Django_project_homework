from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from pytils.translit import slugify
from django.core.mail import send_mail
from catalog.forms import ProductForm, VersionForm, ModeratorForm
from catalog.models import Product, Blog, Version
from catalog.services import get_cached_objects_for_products


# def index(request):
#     context = {
#         'object_list': Product.objects.all(),
#         'title': 'ВЫБЕРИТЕ ДЛЯ СЕБЯ',
#     }
#     return render(request, 'catalog/index.html', context)

# @login_required(login_url='users/')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/index.html'
    extra_context = {
        'title': 'ВЫБЕРИТЕ ДЛЯ СЕБЯ'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = get_cached_objects_for_products()
        return context_data


# def auto_info(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object': product_item,
#         'title': f'Подробнее о {product_item.name}'
#     }
#     return render(request, 'catalog/product_list.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        product_item = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['object'] = product_item
        context_data['title'] = f'Подробнее о {product_item.name}'

        context_data['category_pk'] = product_item.category.pk

        version_item = Version.objects.filter(product=product_item.pk, is_active=True).first()

        if version_item:
            context_data['active_version_number'] = version_item.num_version
            context_data['active_version_name'] = version_item.name_version
        else:
            context_data['active_version_number'] = 'отсутствует'
            context_data['active_version_name'] = '-'

        return context_data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy('catalog:index')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'

    # success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('catalog:product_update', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.is_staff and self.request.user.groups.filter(
                name='Модератор').exists():
            return ModeratorForm
        return ProductForm

    def test_func(self):
        _user = self.request.user
        _instance: Product = self.get_object()
        custom_perms: tuple = (
            'catalog_change.set_is_published',
            'catalog_change.set_category',
            'catalog_change.set_descriptions',
        )
        if _user.is_superuser or _user == _instance.owner:
            return True
        elif _user.groups.filter(name='Модератор') and _user.has_perms(custom_perms):
            return True
        return self.handle_no_permission()


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'image')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('title', 'content')

    # success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
