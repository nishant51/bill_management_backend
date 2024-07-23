from django.urls import path, include
from rest_framework.routers import DefaultRouter

from dashboard.viewsets import ForgotPasswordApi, resetpassword
from .viewsets import CategoryViewSet, LatestInvoiceBillView, ProductViewSet, InvoiceItemViewSet, InvoiceBillViewSet, SubCategoryViewSet, separateCategoryViewSet, separateSubCategoryViewSet

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'allCategory', separateCategoryViewSet, basename='seperate-category')
router.register(r'sub-category', SubCategoryViewSet, basename='sub-catergory')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'InvoiceItems', InvoiceItemViewSet, basename='soldproduct')
router.register(r'InvoiceBills', InvoiceBillViewSet, basename='InvoiceBill')

urlpatterns = [
    path('', include(router.urls)),
    path('allSubCategory/<int:category_id>/', separateSubCategoryViewSet.as_view({'get': 'list'}), name='subcategory-list'),
    path('invoicebills/total_paid/', InvoiceBillViewSet.as_view({'get': 'total_paid'}), name='total-paid'),
    path('invoicebills/total_credit/', InvoiceBillViewSet.as_view({'get': 'total_credit'}), name='total_credit'),
    path('invoicebills/total_bill_price/', InvoiceBillViewSet.as_view({'get': 'total_bill_price'}), name='total_bill_price'),

    path("forgot-password/generate/",ForgotPasswordApi.as_view({"post": "Generate"}), name="forgotpassword-generate"),
    path("forgot-password/verify/", ForgotPasswordApi.as_view({"post": "verify"}), name="forgotpassword-verify" ),
    path("reset-password/", resetpassword, name="resetpassword"),
    
    path('latest-invoice-bill/', LatestInvoiceBillView.as_view(), name='latest-invoice-bill'),


]
