# Generated by Django 4.1 on 2023-03-09 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0018_alter_clients_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='filial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients', to='admins.userinfo'),
        ),
    ]
