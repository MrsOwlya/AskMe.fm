# Generated by Django 2.2.12 on 2021-05-25 22:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0010_auto_20210525_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ask',
            name='ask_tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
