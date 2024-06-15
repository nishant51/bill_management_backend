from django.contrib import admin
from .models import Product, InvoiceItem, DailySalesReport
from .models import Category, SubCategory

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SubCategoryInline]

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'quantity', 'added_date', 'updated_date', 'empty_date', 'category', 'sub_category')
    search_fields = ('name', 'category__name', 'sub_category__name')
    list_filter = ('category', 'sub_category')
    readonly_fields = ('added_date', 'updated_date')
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'quantity', 'category', 'sub_category')
        }),
        ('Dates', {
            'fields': ('added_date', 'updated_date', 'empty_date')
        }),
    )

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total_price', 'created_at', 'discount')
    search_fields = ('product__name',)

@admin.register(DailySalesReport)
class DailySalesReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'sold_product')
    search_fields = ('sold_product__product__name',)
