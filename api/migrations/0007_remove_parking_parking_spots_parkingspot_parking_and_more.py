# Generated by Django 4.2.7 on 2023-11-25 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_space_empty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parking',
            name='parking_spots',
        ),
        migrations.AddField(
            model_name='parkingspot',
            name='parking',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='api.parking'),
        ),
        migrations.AlterField(
            model_name='parkingspot',
            name='is_empty',
            field=models.BooleanField(default=True),
        ),
    ]
