# Generated by Django 4.1 on 2023-03-09 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0019_alter_clients_filial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='spouse_adres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Adres'),
        ),
        migrations.AddField(
            model_name='clients',
            name='spouse_birth_adres',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Birth adress'),
        ),
        migrations.AddField(
            model_name='clients',
            name='spouse_nbm',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nbm'),
        ),
        migrations.AddField(
            model_name='clients',
            name='spouse_sex',
            field=models.CharField(blank=True, choices=[('Erkak', 'Erkak'), ('Ayol', 'Ayol')], max_length=255, null=True, verbose_name='Sex'),
        ),
        migrations.AddField(
            model_name='clients',
            name='spouse_state',
            field=models.CharField(blank=True, choices=[('1', 'Андижанская область'), ('2', 'Бухарская область'), ('3', 'Джизакская область'), ('4', 'Кашкадарьинская область'), ('5', 'Навоийская область'), ('6', 'Наманганская область'), ('7', 'Самаркандская область'), ('8', 'Сурхандарьинская область'), ('9', 'Сырдарьинская область'), ('10', 'Ташкентская область'), ('11', 'Ферганская область'), ('12', 'Хорезмская область'), ('13', 'Республика Каракалпакстан'), ('14', 'Город Ташкент')], max_length=255, null=True, verbose_name='State'),
        ),
    ]
