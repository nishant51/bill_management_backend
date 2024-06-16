# your_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceItem

@receiver(post_save, sender=InvoiceItem)
def reduce_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.in_stock -= instance.quantity
        product.save()
