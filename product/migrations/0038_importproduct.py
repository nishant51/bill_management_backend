# Generated by Django 5.0.6 on 2024-08-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_trackinginvoicebillid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amt', models.FloatField(blank=True, null=True)),
                ('paid_amt', models.FloatField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice_miti', models.DateField()),
                ('Bill_no', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
