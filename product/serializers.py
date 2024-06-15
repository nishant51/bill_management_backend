from rest_framework import serializers
from .models import Category, Product, InvoiceItem, InvoiceBill, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    sub_category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category(self, obj):
        if obj.category:
            return {'value': obj.category.id, 'label': obj.category.name if obj.category else None}
        return None

    def get_sub_category(self, obj):
        if obj.sub_category:
            return {'value': obj.sub_category.id, 'label': obj.sub_category.name if obj.sub_category else None}
        return None


class InvoiceItemSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = '__all__'

    def get_product_info(self, obj):
        if obj.product:
            return {'value': obj.product.id, 'label': obj.product.name}
        return None

class InvoiceBillSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceBill
        fields = '__all__'

    def get_product_info(self, obj):
        if obj.sold_product and obj.sold_product.product:
            return {'value': obj.sold_product.product.id, 'label': obj.sold_product.product.name}
        return None

