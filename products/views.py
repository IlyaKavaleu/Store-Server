from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from common.views import TitleMixin
from .models import Product, ProductCategory, Basket
from users.models import User
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.core.cache import cache


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    title = 'Store - Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 10)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):
    Basket.create_or_update(product_id, request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def all_quantity_in_basket(request):
#     baskets = Basket.objects.filter(user=request.user)
#     context = {'baskets': baskets}
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def price_this_product(request, product_id):
#     product = Product.objects.get(id=product_id)
#     basket = Basket.objects.filter(user=request.user, product=product)
#
#     price_and_quantity_this_product = basket.product.quantity * basket.product.price
#     context = {'price_and_quantity_this_product': price_and_quantity_this_product}
#     return render(request, 'products/baskets.html', context)
