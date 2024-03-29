from django.contrib import admin
from .models import ProductCategory, Product, Basket


admin.site.register(ProductCategory)
# admin.site.register(Product)
# admin.site.register(Basket)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'image', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('quantity',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0
