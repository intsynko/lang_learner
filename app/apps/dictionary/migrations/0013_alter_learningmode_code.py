# Generated by Django 4.1.3 on 2022-11-30 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0012_learningmode_dictionary_learning_mods'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningmode',
            name='code',
            field=models.CharField(max_length=50, verbose_name='Code'),
        ),
    ]
