# Generated by Django 5.0.6 on 2024-08-05 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0040_alter_invoicebill_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicebill',
            name='bill_pdf',
            field=models.FileField(blank=True, null=True, upload_to='bill_pdf/'),
        ),
    ]
