from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Product, InvoiceItem, InvoiceBill, SubCategory, TrackingInvoiceBillId
from .serializers import CategorySerializer, ProductSerializer, InvoiceItemSerializer, InvoiceBillSerializer, SeparateCategorySerializer, SubCategorySerializer
from rest_framework.permissions import IsAuthenticated
from .paginations import EightPagination, FivePagination, TenPagination
from django.db.models import Q
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta, time
from rest_framework.decorators import action
from django.db.models import Sum

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by("-id")
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all().order_by("id")
    serializer_class = SubCategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework.exceptions import NotFound


class separateSubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer
    # pagination_class = FivePagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        queryset = SubCategory.objects.filter(category_id=category_id)
        query = self.request.query_params.get('search_name', None)
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'results': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})

class separateCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all().order_by("-id")
    serializer_class = SeparateCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.query_params.get('search_name', None)
        category = self.request.query_params.get('category', None)

        if search_name:
            queryset &= Q(name__icontains=search_name)
        if category:
            queryset &= Q(category=category)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'results': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'results': serializer.data})

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = EightPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.query_params.get('search_name', None)
        category = self.request.query_params.get('category', None)

        if search_name:
            queryset = queryset.filter(Q(name__icontains=search_name))
        if category:
            queryset = queryset.filter(Q(category=category))
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        category_id = request.data.get('category')
        sub_category_id = request.data.get('sub_category')
        
        category = None
        sub_category = None
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        if sub_category_id:
            try:
                sub_category = SubCategory.objects.get(id=sub_category_id)
            except SubCategory.DoesNotExist:
                return Response({"detail": "Sub-category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(category=category, sub_category=sub_category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        category_id = request.data.get('category')
        sub_category_id = request.data.get('sub_category')
        
        category = None
        sub_category = None
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        if sub_category_id:
            try:
                sub_category = SubCategory.objects.get(id=sub_category_id)
            except SubCategory.DoesNotExist:
                return Response({"detail": "Sub-category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save(category=category, sub_category=sub_category)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class InvoiceItemViewSet(viewsets.ModelViewSet):
    queryset = InvoiceItem.objects.filter(sold_out = False).order_by("-id")
    serializer_class = InvoiceItemSerializer
    # pagination_class = FivePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_name = self.request.query_params.get('search_name', None)

        if search_name:
            queryset = queryset.filter(Q(name__icontains=search_name))
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     # page = self.paginate_queryset(queryset)
    #     # if page is not None:
    #     #     serializer = self.get_serializer(page, many=True)
    #     #     return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class InvoiceBillViewSet(viewsets.ModelViewSet):
    queryset = InvoiceBill.objects.order_by("-id")
    serializer_class = InvoiceBillSerializer
    pagination_class = TenPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        customer_name = self.request.query_params.get('customer_name', None)
        mode_of_payment = self.request.query_params.get('mode_of_payment', None)

        if customer_name:
            queryset = queryset.filter(Q(bill_for__icontains=customer_name))
        if mode_of_payment:
            queryset = queryset.filter(Q(mode_of_payment=mode_of_payment))
            
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance  
        if instance.is_printed:
            instance.Invoice_Item.update(sold_out=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if instance.is_printed:
            instance.Invoice_Item.update(sold_out=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_totals(self, request):
        try:
            # Aggregating the total paid, total credit, and total bill price
            aggregates = InvoiceBill.objects.aggregate(
                total_paid=Sum('paid_amt'),
                total_credit=Sum('credit_amt'),
                total_bill_price=Sum('total_price')
            )

            # Filtering InvoiceItem related to InvoiceBill
            invoice_items = InvoiceItem.objects.filter(invoicebill__isnull=False)

            # Aggregating the total quantity sold and total in-stock quantity
            total_quantity_sold = invoice_items.aggregate(total_sold=Sum('quantity'))['total_sold']
            total_in_stock = Product.objects.aggregate(total_stock=Sum('in_stock'))['total_stock']

            # Aggregating the total sold items by product
            products_sold = invoice_items.values('product__name').annotate(total_sold=Sum('quantity')).order_by('-total_sold')[:6]

            return Response({
                'total_paid_amt': aggregates['total_paid'],
                'total_credit_amt': aggregates['total_credit'],
                'total_bill_price': aggregates['total_bill_price'],
                'total_quantity_sold': total_quantity_sold,
                'total_in_stock': total_in_stock,
                'products_sold': list(products_sold)
            }, status=status.HTTP_200_OK)

        except InvoiceBill.DoesNotExist:
            return Response({
                'error': 'InvoiceBill data does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except InvoiceItem.DoesNotExist:
            return Response({
                'error': 'InvoiceItem data does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Product.DoesNotExist:
            return Response({
                'error': 'Product data does not exist.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

from rest_framework.views import APIView

class LatestInvoiceBillView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            latest_tracking = TrackingInvoiceBillId.objects.latest('id')
            data = {
                'id': latest_tracking.ref_id
            }
            return Response(data, status=status.HTTP_200_OK)
        except TrackingInvoiceBillId.DoesNotExist:
            data = {
                'id': 0
            }
            return Response(data, status=status.HTTP_200_OK)
