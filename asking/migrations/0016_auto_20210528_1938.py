# Generated by Django 2.2.12 on 2021-05-28 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0015_auto_20210528_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_dislikes',
            field=models.IntegerField(default=0, verbose_name='Кол-во дизлайков'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='dislike',
            field=models.BooleanField(default=False, verbose_name='Дизлайк'),
        ),
        migrations.AlterField(
            model_name='answerlike',
            name='like',
            field=models.BooleanField(default=False, verbose_name='Лайк'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_dislikes',
            field=models.IntegerField(default=0, verbose_name='Кол-во дизлайков'),
        ),
        migrations.AlterField(
            model_name='asklike',
            name='dislike',
            field=models.BooleanField(default=False, verbose_name='Дизлайк'),
        ),
        migrations.AlterField(
            model_name='asklike',
            name='like',
            field=models.BooleanField(default=False, verbose_name='Лайк'),
        ),
    ]
