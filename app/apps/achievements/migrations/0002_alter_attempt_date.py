# Generated by Django 4.1.3 on 2022-11-29 21:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
