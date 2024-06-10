from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ProductViewSet, SoldProductViewSet, DailySalesReportViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'soldproducts', SoldProductViewSet, basename='soldproduct')
router.register(r'dailysalesreports', DailySalesReportViewSet, basename='dailysalesreport')

urlpatterns = [
    path('', include(router.urls)),
]
