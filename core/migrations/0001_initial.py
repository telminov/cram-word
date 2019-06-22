# Generated by Django 2.2 on 2019-06-22 18:22

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Язык',
                'verbose_name_plural': 'Языки',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Название')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Раздел',
                'unique_together': {('user', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('to_rus', 'на русский'), ('from_rus', 'с русского')], max_length=255, verbose_name='Направление')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Язык')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Тренировка',
                'verbose_name_plural': 'Тренировки',
            },
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Слово')),
                ('translation', models.CharField(max_length=255, verbose_name='Перевод')),
                ('transcription', models.CharField(blank=True, max_length=255, verbose_name='Транскрипция')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language', verbose_name='Язык')),
                ('sections', models.ManyToManyField(blank=True, to='core.Section', verbose_name='Раздел')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Раздел',
                'unique_together': {('user', 'language', 'name')},
            },
        ),
        migrations.CreateModel(
            name='TrainingWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=255, verbose_name='Ответ')),
                ('is_right', models.NullBooleanField(verbose_name='Правильный ли ответ')),
                ('answer_dt', models.DateTimeField(blank=core.models.Training, null=True, verbose_name='Время ответа')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Training')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Word')),
            ],
        ),
    ]
