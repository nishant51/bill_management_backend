# Generated by Django 5.0.6 on 2024-07-19 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_remove_invoicebill_invoice_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicebill',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]