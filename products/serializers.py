from rest_framework import serializers, fields
from products.models import Product, ProductCategory, Basket


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'quantity', 'image', 'category')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    price_all_products = fields.SerializerMethodField()
    sum_all_products = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'price_all_products', 'sum_all_products', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_price_all_products(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).price_all_products()

    def get_sum_all_products(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).sum_all_products()