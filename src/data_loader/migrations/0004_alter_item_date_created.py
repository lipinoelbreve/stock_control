# Generated by Django 4.1.5 on 2023-01-19 19:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0003_alter_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
