# Generated by Django 4.2.1 on 2023-07-23 16:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0008_item_last_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, default=10, max_digits=6, null=True
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="title",
            field=models.CharField(max_length=500),
        ),
    ]
