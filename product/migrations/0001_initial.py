# Generated by Django 5.0.6 on 2024-06-10 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('image', models.BinaryField(blank=True, null=True)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('added_date', models.DateField()),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('empty_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SoldProduct',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='DailySalesReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sold_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.soldproduct')),
            ],
        ),
    ]
