# Generated by Django 3.1.7 on 2021-03-30 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210330_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='deleted_at',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
