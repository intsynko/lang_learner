# Generated by Django 4.1.3 on 2022-11-21 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_dictionary_pinned_alter_rate_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Words',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('word_from', models.CharField(max_length=50, verbose_name='Word from')),
                ('word_to', models.CharField(max_length=50, verbose_name='Word from')),
                ('active', models.BooleanField(default=True)),
                ('example_1', models.CharField(max_length=255, verbose_name='Example 1')),
                ('example_2', models.CharField(max_length=255, verbose_name='Example 2')),
                ('frequency', models.SmallIntegerField(default=10, verbose_name='Frequency')),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='dictionary.dictionary', verbose_name='Dictionary')),
            ],
        ),
    ]