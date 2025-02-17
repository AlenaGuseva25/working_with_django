from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from catalog.models import Product



def home_catalog(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/home.html', context)


def contacts_catalog(request):
    return render(request, 'catalog/contacts.html')


def product_list(request):
    products = Product.objects.all()
    context = {'products': products,}
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product' : product,
    }
    return render(request, 'catalog/product_detail.html', context=context)