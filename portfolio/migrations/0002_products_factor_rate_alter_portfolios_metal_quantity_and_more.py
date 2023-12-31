# Generated by Django 4.2.3 on 2023-09-04 12:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="products",
            name="factor_rate",
            field=models.DecimalField(
                decimal_places=4, default=0.0, max_digits=8, verbose_name="Factor Rate"
            ),
        ),
        migrations.AlterField(
            model_name="portfolios",
            name="metal_quantity",
            field=models.IntegerField(default=0, verbose_name="Quantity"),
        ),
        migrations.AlterField(
            model_name="portfolios",
            name="metal_value",
            field=models.DecimalField(
                decimal_places=4, default=0.0, max_digits=10, verbose_name="Metal Value"
            ),
        ),
        migrations.AlterField(
            model_name="portfolios",
            name="purchase_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 4, 12, 18, 48, 12809, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Purchase Date",
            ),
        ),
        migrations.AlterField(
            model_name="portfolios",
            name="sku",
            field=models.CharField(default="-", max_length=20, verbose_name="SKU"),
        ),
    ]
