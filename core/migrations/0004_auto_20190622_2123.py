# Generated by Django 2.2 on 2019-06-22 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20190622_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingword',
            name='answer_options',
            field=models.ManyToManyField(to='core.Word'),
        ),
        migrations.AlterField(
            model_name='trainingword',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_words', to='core.Training'),
        ),
        migrations.AlterField(
            model_name='trainingword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_words', to='core.Word'),
        ),
    ]
