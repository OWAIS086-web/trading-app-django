# Generated by Django 4.2.3 on 2023-09-05 06:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0003_alter_portfolios_purchase_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="portfolios",
            name="purchase_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 9, 5, 6, 1, 16, 901003, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Purchase Date",
            ),
        ),
    ]