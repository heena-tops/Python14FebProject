# Generated by Django 4.2 on 2023-05-13 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0015_alter_cart_product_price_alter_cart_product_qty_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razorpay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
