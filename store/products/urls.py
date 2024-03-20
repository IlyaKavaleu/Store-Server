from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


app_name = 'products'

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>', views.ProductsListView.as_view(), name='category'),
    path('page/<int:page>', views.ProductsListView.as_view(), name='paginator'),

    path('baskets/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', views.basket_remove, name='basket_remove'),
]
