# Generated by Django 4.1.5 on 2023-01-26 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0015_alter_account_available_qty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='item_count',
            field=models.IntegerField(default=0),
        ),
    ]
