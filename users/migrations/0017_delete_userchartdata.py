# Generated by Django 4.2.4 on 2023-08-25 10:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0016_userchartdata"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserChartData",
        ),
    ]