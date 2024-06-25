from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Category, Product, InvoiceItem, InvoiceBill, SubCategory
from .serializers import CategorySerializer, ProductSerializer, InvoiceItemSerializer, InvoiceBillSerializer, SeparateCategorySerializer, SubCategorySerializer
from rest_framework.permissions import IsAuthenticated
from .paginations import FivePagination, TenPagination
from django.db.models import Q


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
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
    queryset = SubCategory.objects.all()
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
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = SeparateCategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    pagination_class = TenPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('search_name', None)
        if query:
            # Filter queryset based on the 'q' parameter
            queryset = queryset.filter(
                Q(name__icontains=query)  #| 
                # Q(description__icontains=query)  # Example: Filter by description
            )
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
        query = self.request.query_params.get('search_name', None)
        if query:
            queryset = queryset.filter(
                Q(product__name__icontains=query)  #| 
                # Q(description__icontains=query)  
            )
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
    queryset = InvoiceBill.objects.all()
    serializer_class = InvoiceBillSerializer
    pagination_class = TenPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.query_params.get('search_name', None)
        if query:
            queryset = queryset.filter(
                Q(sold_product__product__name__icontains=query)  #| 
            )
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
        instance = serializer.instance  # Get the created instance
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
   