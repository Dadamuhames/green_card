# Generated by Django 4.1 on 2023-03-07 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0012_alter_clients_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='agent_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Agent name'),
        ),
    ]
