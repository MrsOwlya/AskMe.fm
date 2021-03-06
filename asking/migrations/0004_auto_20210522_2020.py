# Generated by Django 2.2.12 on 2021-05-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asking', '0003_auto_20210520_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_likes',
            field=models.IntegerField(default=0, verbose_name='Кол-во лайков'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_answers',
            field=models.IntegerField(default=0, verbose_name='Кол-во ответов'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='ask',
            name='ask_rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг вопроса'),
        ),
        migrations.AlterField(
            model_name='like',
            name='likes_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во лайков'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_rating',
            field=models.IntegerField(default=1, verbose_name='Популярность тега'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_avatar',
            field=models.ImageField(blank=True, null=True, upload_to='static/asking/img', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_rating',
            field=models.IntegerField(blank=True, default=0, verbose_name='Рейтинг'),
        ),
    ]
