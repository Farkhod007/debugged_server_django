# Generated by Django 3.1.7 on 2021-03-27 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.TimeField(blank=True, default=None),
        ),
        migrations.AlterModelTable(
            name='post',
            table='posts',
        ),
    ]
