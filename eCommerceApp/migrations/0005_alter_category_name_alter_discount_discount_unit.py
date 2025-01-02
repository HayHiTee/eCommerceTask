# Generated by Django 5.1.4 on 2025-01-02 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCommerceApp', '0004_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_unit',
            field=models.CharField(choices=[('fixed', 'Fixed Price'), ('percent', 'Percentage')], max_length=10),
        ),
    ]