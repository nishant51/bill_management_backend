from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import InvoiceItem

@receiver(pre_save, sender=InvoiceItem)
def update_product_stock(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = InvoiceItem.objects.get(pk=instance.pk)
        product = instance.product
        difference = instance.quantity - previous_instance.quantity
        product.in_stock -= difference
        product.save()
    else:
        product = instance.product
        product.in_stock -= instance.quantity
        product.save()
