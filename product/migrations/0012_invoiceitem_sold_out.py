# Generated by Django 5.0.6 on 2024-06-25 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_alter_invoicebill_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='sold_out',
            field=models.BooleanField(default=False),
        ),
    ]