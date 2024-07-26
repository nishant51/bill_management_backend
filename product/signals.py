from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import InvoiceItem
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .models import InvoiceBill

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

# # signals.py


# @receiver(post_save, sender=InvoiceBill)
# def update_sold_out(sender, instance, created, **kwargs):
#     if instance.is_printed:
#         instance.Invoice_Item.update(sold_out=True)

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=InvoiceItem)
def update_product_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.in_stock += instance.quantity
    product.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InvoiceBill, TrackingInvoiceBillId

@receiver(post_save, sender=InvoiceBill)
def update_tracking_invoice_bill_id(sender, instance, created, **kwargs):
    if created:
        TrackingInvoiceBillId.objects.all().delete()
        
        TrackingInvoiceBillId.objects.create(ref_id=str(instance.id))
