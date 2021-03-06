# Generated by Django 2.2 on 2019-06-22 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ('name',), 'verbose_name': 'Язык', 'verbose_name_plural': 'Языки'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ('name',), 'verbose_name': 'Раздел', 'verbose_name_plural': 'Раздел'},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'ordering': ('name',), 'verbose_name': 'Слово', 'verbose_name_plural': 'Слова'},
        ),
        migrations.AddField(
            model_name='training',
            name='mode',
            field=models.CharField(choices=[('все слова', 'все слова'), ('неизученные', 'неизученные')], default=1, max_length=255, verbose_name='Режим'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='training',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='trainings', to='core.Section', verbose_name='Раздел'),
        ),
        migrations.AlterField(
            model_name='training',
            name='direction',
            field=models.CharField(choices=[('на русский', 'на русский'), ('с русского', 'с русского')], max_length=255, verbose_name='Направление'),
        ),
        migrations.AlterField(
            model_name='word',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='words', to='core.Section', verbose_name='Раздел'),
        ),
    ]
