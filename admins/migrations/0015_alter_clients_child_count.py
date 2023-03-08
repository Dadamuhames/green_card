# Generated by Django 4.1 on 2023-03-08 10:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0014_clients_child_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='child_count',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Child count'),
        ),
    ]
