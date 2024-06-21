from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CategoryViewSet, ProductViewSet, InvoiceItemViewSet, InvoiceBillViewSet, SubCategoryViewSet, separateCategoryViewSet

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'seperate-Category-ViewSet', separateCategoryViewSet, basename='seperate-category')
router.register(r'sub-category', SubCategoryViewSet, basename='sub-catergory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'InvoiceItems', InvoiceItemViewSet, basename='soldproduct')
router.register(r'InvoiceBills', InvoiceBillViewSet, basename='InvoiceBill')

urlpatterns = [
    path('', include(router.urls)),
]
