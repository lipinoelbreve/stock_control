# Generated by Django 4.1.5 on 2023-01-25 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0010_alter_item_trello'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movement',
            old_name='person',
            new_name='user',
        ),
    ]
