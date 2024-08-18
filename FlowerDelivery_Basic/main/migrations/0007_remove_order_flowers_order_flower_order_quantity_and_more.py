# Generated by Django 5.0.7 on 2024-08-14 10:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_order_flowers_alter_order_total_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='flowers',
        ),
        migrations.AddField(
            model_name='order',
            name='flower',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.flower'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='OrderFlower',
        ),
    ]
