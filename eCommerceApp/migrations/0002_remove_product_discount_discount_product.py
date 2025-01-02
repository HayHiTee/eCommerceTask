# Generated by Django 5.1.4 on 2025-01-02 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerceApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='eCommerceApp.product'),
        ),
    ]