# Generated by Django 5.1.4 on 2025-01-02 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerceApp', '0003_alter_discount_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('fixed', 'Fixed Price'), ('percent', 'Percentage')], max_length=10),
        ),
    ]
