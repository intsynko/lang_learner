# Generated by Django 4.1.3 on 2022-12-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0013_alter_learningmode_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='words',
            name='transcription',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Transcription'),
        ),
    ]
