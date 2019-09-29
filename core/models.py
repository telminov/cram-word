from typing import Optional

from django.db import models
from django.contrib.auth import get_user_model
from core import consts


User = get_user_model()


class Language(models.Model):
    CODE_CHOICES = (
        ('en', 'Английский'),
        ('fr', 'Французский'),
    )

    name = models.CharField('Название', max_length=255, unique=True)
    code = models.CharField('Код', max_length=10, default='en', choices=CODE_CHOICES)

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

    def get_language(self) -> Optional[Language]:
        first_word = self.words.all().first()
        if first_word:
            return first_word.language


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

    @staticmethod
    def filter_unknown(words):
        unknown = []
        for w in words:
            trainings = w.trainigs.filter(answer_dt__isnull=False).order_by('answer_dt')
            if not trainings.exists() or not trainings.last().is_right:
                unknown.append(w)
        return unknown


class Training(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    language = models.ForeignKey(Language, verbose_name='Язык', on_delete=models.CASCADE)
    sections = models.ManyToManyField(Section, verbose_name='Раздел', blank=True, related_name='trainings')
    direction = models.CharField('Направление', max_length=255, choices=consts.DIRECTION_CHOICES,
                                 default=consts.DIRECTION_TO_RUS)
    mode = models.CharField('Режим', max_length=255, choices=consts.TRAINING_MODE_CHOICES,
                            default=consts.TRAINING_MODE_ALL_WORDS, )
    created = models.DateTimeField(auto_now_add=True)
    canceled = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'


class TrainingWord(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='training_words')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='training_words')
    answer = models.CharField('Ответ', max_length=255, blank=True)
    is_right = models.NullBooleanField('Правильный ли ответ')
    answer_dt = models.DateTimeField('Время ответа', null=True, blank=Training)
    answer_options = models.ManyToManyField(Word)


