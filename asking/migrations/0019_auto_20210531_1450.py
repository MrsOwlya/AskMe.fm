# Generated by Django 2.2.12 on 2021-05-31 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0018_auto_20210531_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/asking/img/', verbose_name='Аватарка'),
        ),
    ]
