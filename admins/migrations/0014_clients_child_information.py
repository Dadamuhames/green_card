# Generated by Django 4.1 on 2023-03-08 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0013_clients_agent_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='child_information',
            field=models.TextField(blank=True, null=True, verbose_name='Child inf'),
        ),
    ]