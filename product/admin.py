from django.contrib import admin
from .models import  ImportProduct, Product, InvoiceItem, InvoiceBill
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
    list_display = ('id', 'name', 'price', 'in_stock', 'added_date', 'updated_date', 'empty_date', 'category', 'sub_category')
    search_fields = ('name', 'category__name', 'sub_category__name')
    list_filter = ('category', 'sub_category')
    readonly_fields = ('added_date', 'updated_date')
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'category', 'sub_category')
        }),
        ('Dates', {
            'fields': ('added_date', 'updated_date', 'empty_date')
        }),
    )

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'total_price', 'created_at', 'discount', 'sold_out')
    search_fields = ('product__name',)

# @admin.register(InvoiceBill)
# class InvoiceBillAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'display_Invoice_Item', 'bill_for', 'is_printed', 'pdf')
#     search_fields = ('Invoice_Item__name',)

#     def display_Invoice_Item(self, obj):
#         items = [item.product.name for item in obj.Invoice_Item.all()]
#         print(f"Items: {items}")
#         return ", ".join(items) if items else "No Products"
admin.site.register(InvoiceBill)




@admin.register(ImportProduct)
class ImportProductAdmin(admin.ModelAdmin):
    list_display = ('Bill_no', 'name', 'quantity', 'total_amount', 'credit_amt', 'paid_amt', 'mode_of_payment', 'invoice_miti')
    search_fields = ('Bill_no', 'name')
    list_filter = ('mode_of_payment', 'invoice_miti')
    ordering = ('-invoice_miti',)
    readonly_fields = ('total_amount', 'credit_amt', 'paid_amt')

    fieldsets = (
        (None, {
            'fields': ('name', 'quantity', 'total_amount', 'credit_amt', 'paid_amt', 'mode_of_payment', 'invoice_miti', 'Bill_no')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('Bill_no',)
        return self.readonly_fields