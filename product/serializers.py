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
    

class SeparateCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    total_subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories', 'total_subcategories')

    def get_total_subcategories(self, obj):
        try:
            return obj.subcategories.count()  # Assuming subcategories is a related manager
        except Exception as e:
            raise serializers.ValidationError(f"Failed to retrieve total subcategories: {str(e)}")


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
            return {'value': obj.product.id, 'label': obj.product.name, 'price':obj.product.price, 'in_stock':obj.product.in_stock}
        return None

class InvoiceBillSerializer(serializers.ModelSerializer):
    product_info = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceBill
        fields = '__all__'

    def get_product_info(self, obj):
        product_info = []
        for invoice_item in obj.sold_product.all():
            product = invoice_item.product  # Assuming InvoiceItem has a 'product' ForeignKey field
            product_info.append({
                'value': product.id,
                'label': product.name
            })
        return product_info if product_info else None

