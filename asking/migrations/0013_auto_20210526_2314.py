# Generated by Django 2.2.12 on 2021-05-26 23:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asking', '0012_answer_answer_is_right'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Кол-во лайков')),
                ('dislike', models.BooleanField(default=False, verbose_name='Кол-во дизлайков')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asking.Answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AskLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Кол-во лайков')),
                ('dislike', models.BooleanField(default=False, verbose_name='Кол-во дизлайков')),
                ('ask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asking.Ask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
