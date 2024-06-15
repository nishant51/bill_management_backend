from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet, ProductViewSet, InvoiceItemViewSet, DailySalesReportViewSet, SubCategoryViewSet

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'sub-category', SubCategoryViewSet, basename='sub-catergory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'InvoiceItems', InvoiceItemViewSet, basename='soldproduct')
router.register(r'dailysalesreports', DailySalesReportViewSet, basename='dailysalesreport')

urlpatterns = [
    path('', include(router.urls)),
]
