from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.BinaryField(null=True, blank=True)
    price = models.IntegerField()
    in_stock = models.IntegerField()
    added_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    empty_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, related_name='products_sub_category', on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.name

class InvoiceItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(blank=True, null=True)
    sold_out= models.BooleanField(default=False)


    def __str__(self):
        return f"Sold {self.quantity} of {self.product.name}"

class InvoiceBill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500, blank=True, null= True)
    Invoice_Item = models.ManyToManyField('InvoiceItem')
    address = models.CharField(max_length=600, blank= True, null= True)
    invoice_number = models.CharField(max_length=200, blank=True , null=True)
    total_price = models.FloatField(blank=True, null=True)
    credit_amt = models.FloatField(blank=True, null=True)
    paid_amt = models.FloatField(blank=True, null=True)
    mode_of_payment= models.CharField(max_length=250, blank= True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    bill_for = models.CharField(max_length=500, blank=True, null=True)
    is_printed= models.BooleanField(default=False)
    remark = models.TextField(blank= True,  null= True)

    def __str__(self):
        return f"invoice bill ID: {self.id}"
