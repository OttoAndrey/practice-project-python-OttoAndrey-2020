# Generated by Django 3.0.8 on 2020-07-30 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_auto_20200730_2107'),
        ('catering', '0003_auto_20200727_2056'),
    ]

    operations = [
        migrations.AddField(
            model_name='catering',
            name='dishes',
            field=models.ManyToManyField(to='dish.Dish', verbose_name='Блюда'),
        ),
    ]