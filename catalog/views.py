from django.shortcuts import render

from catalog.models import Product


def index(request):
    context = {
        'object_list': Product.objects.all(),
        'title': 'ВЫБЕРИТЕ ДЛЯ СЕБЯ',
    }
    return render(request, 'catalog/index.html', context)


def auto_info(request, pk):
    category_item = Product.objects.get(pk=pk)
    context = {
        'object': category_item,
        'title': f'Подробнее о {category_item.name}'
    }
    return render(request, 'catalog/auto_info.html', context)

# def catalog_auto(request, pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': f'Автомобили {category_item.name}а',
#     }
#     return render(request, 'catalog/catalog_auto.html', context)


# def contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')
#         print(f'You have new message from {name}({phone}): {message}')
#     return render(request,
