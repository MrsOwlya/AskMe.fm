# Generated by Django 2.2.12 on 2021-05-31 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0016_auto_20210528_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/asking/img/', verbose_name='Аватарка'),
        ),
    ]
