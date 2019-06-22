from django.db import models
from django.contrib.auth import get_user_model
from core import consts


User = get_user_model()


class Language(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'
        ordering = ('name', )

    def __str__(self):
        return self.name


class Section(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=255, unique=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Раздел'
        unique_together = ('user', 'name')
        ordering = ('name', )

    def __str__(self):
        return self.name


class Word(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.CASCADE)
    name = models.CharField('Слово', max_length=255)
    translation = models.CharField('Перевод', max_length=255)
    transcription = models.CharField('Транскрипция', max_length=255, blank=True)
    sections = models.ManyToManyField(Section, verbose_name='Раздел', blank=True, related_name='words')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'
        unique_together = ('user', 'language', 'name')
        ordering = ('name', )

    def __str__(self):
        return self.name


class Training(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.CASCADE)
    direction = models.CharField('Направление', max_length=255, choices=consts.DIRECTION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'


class TrainingWord(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    answer = models.CharField('Ответ', max_length=255, blank=True)
    is_right = models.NullBooleanField('Правильный ли ответ')
    answer_dt = models.DateTimeField('Время ответа', null=True, blank=Training)



