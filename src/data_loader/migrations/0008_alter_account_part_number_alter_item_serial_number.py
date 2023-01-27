# Generated by Django 4.1.5 on 2023-01-24 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0007_alter_item_account_alter_item_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='part_number',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='serial_number',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]