# Generated by Django 3.0.8 on 2020-07-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.IntegerField(verbose_name='Стоимость'),
        ),
    ]
