# Generated by Django 5.0.6 on 2024-07-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_invoicebill_contact_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicebill',
            name='unit',
            field=models.CharField(blank=True, null=True),
        ),
    ]