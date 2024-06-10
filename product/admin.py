from django.contrib import admin
from .models import Product, SoldProduct, DailySalesReport

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'added_date', 'updated_date', 'empty_date')
    search_fields = ('name',)

@admin.register(SoldProduct)
class SoldProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total_price', 'created_at', 'discount')
    search_fields = ('product__name',)

@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'sold_product')
    search_fields = ('sold_product__product__name',)
