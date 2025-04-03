from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_products_by_category
from django.core.cache import cache
from django.db.models import F



from catalog.forms import ProductForm, ProductModeratorForm
from catalog.models import Product, Category
from catalog.services import get_products_by_category
from config.settings import MODERATOR_GROUP


class HomeCatalogView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        "Только опубликованные продукты"
        return Product.objects.filter(is_published=True)

class ContactsCatalogView(View):
    def get(self, request):
        return render(request, 'catalog/contacts.html')


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=MODERATOR_GROUP).exists():
            return Product.objects.all()
        return Product.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = cache.get('product_list')
        if products is None:
            products = list(Product.objects.annotate(views_count_display=F('views_count')).filter(
                is_published=True).order_by('name'))
            cache.set('product_list', products, timeout=60 * 10)
        context['products'] = products
        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'pk'

    def get_object(self):
        obj = super().get_object()
        obj.views_count += 1
        obj.save()
        return obj

    # @method_decorator(cache_page(60 * 5))
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:products')

    def has_permission(self):
        if not self.request.user.groups.filter(name__in=MODERATOR_GROUP).exists():
            return self.request.user.is_active

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_update.html'
    success_url = reverse_lazy('catalog:products')

    def get_success_url(self):
        return reverse_lazy("catalog:products")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if user.groups.filter(name=MODERATOR_GROUP).exists():
            return ProductModeratorForm
        return PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm('catalog.delete_product')

class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.is_published:
            product.is_published = False
            product.save()
            return redirect('catalog:product', pk=pk)
        else:
            product.is_published = True
            product.save()
            return redirect('catalog:product', pk=pk)


    def get_object(self):
        return get_object_or_404(Product, pk=self.kwargs['pk'])


class ProductByCategoryView(ListView):
    model = Product
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

def categories_processor(request):
    "Список категорий в каждом шаблоне"
    categories = Category.objects.all()
    return {'categories': categories}