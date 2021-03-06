# Generated by Django 3.0.8 on 2020-08-03 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dish', '0002_auto_20200730_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dish',
            name='sum_of_calories',
            field=models.FloatField(default=0.0, null=True, verbose_name='Сумма калорий'),
        ),
    ]
