from django.contrib import admin
from core import models


class TrainingWordInline(admin.TabularInline):
    model = models.TrainingWord
    extra = 0


class Training(admin.ModelAdmin):
    inlines = (TrainingWordInline, )


class Word(admin.ModelAdmin):
    list_display = ('name', 'translation', 'transcription', 'user', 'language', )
    list_display_links = ('name', )
    list_filter = ('user', 'language', 'sections')


admin.site.register(models.Language)
admin.site.register(models.Section)
admin.site.register(models.Word, Word)
admin.site.register(models.Training, Training)