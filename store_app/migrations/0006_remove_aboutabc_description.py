# Generated by Django 4.1.3 on 2022-12-01 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_aboutabc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutabc',
            name='description',
        ),
    ]