from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.BinaryField(blank=True, null=True)
    price = models.IntegerField()
    quantity = models.IntegerField()
    added_date = models.DateField()
    updated_date = models.DateField(blank=True, null=True)
    empty_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class SoldProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Sold {self.quantity} of {self.product.name}"

class DailySalesReport(models.Model):
    id = models.AutoField(primary_key=True)
    sold_product = models.ForeignKey(SoldProduct, on_delete=models.CASCADE)

    def __str__(self):
        return f"Daily Report ID: {self.id}"
