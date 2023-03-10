# Generated by Django 4.1.5 on 2023-01-25 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_loader', '0008_alter_account_part_number_alter_item_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='last_movement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='data_loader.movement'),
        ),
        migrations.AddField(
            model_name='movement',
            name='movement_type',
            field=models.CharField(blank=True, choices=[('creation', 'Creation'), ('transfer', 'Transfer'), ('repair', 'Repair'), ('destroyed', 'Destroyed')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='data_loader.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(blank=True, choices=[('available', 'Available'), ('in_use', 'In Use'), ('repair', 'Repair'), ('disposed', 'Disposed')], max_length=100, null=True),
        ),
    ]
