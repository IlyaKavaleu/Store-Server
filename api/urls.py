from django.urls import path, include
from api.views import BasketModelViewSet, ProductModelViewSet
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'
router = DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'baskets', BasketModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('products/', ProductModelViewSet.as_view(), name='products'),
    # path('products/<int:pk>', ProductDetailViewSet.as_view(), name='products-detail'),
    # path('baskets/', BasketModelViewSet.as_view(), name='baskets'),
    # path('baskets/<int:pk>', BasketDetailViewSet.as_view(), name='basket-detail'),
]

