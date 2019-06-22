from django.contrib import messages
from django.urls import reverse_lazy, reverse

from django.views.generic import TemplateView, CreateView
from core import models
from core import consts


class Create(CreateView):
    template_name = 'core/object_create.html'
    model = models.Training
    fields = ('language', 'sections', 'direction',  'mode', )
    success_url = reverse_lazy('core:index')    # TODO

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('section'):
            section = models.Section.objects.get(id=self.request.GET['section'])
            initial['sections'] = [section.pk]

            trainings = models.Training.objects.filter(user=self.request.user)
            if trainings.exists():
                initial['language'] = trainings.last().language
        return initial

    def form_valid(self, form):
        words = models.Word.objects.filter(
            user=self.request.user,
            language=form.cleaned_data['language'],
        )
        if form.cleaned_data['sections']:
            words = words.filter(sections__in=form.cleaned_data['sections'])
        if form.cleaned_data['mode'] == consts.TRAINING_MODE_UNKNOWN_WORDS:
            words = models.Word.filter_unknown(words)

        if not words:
            messages.error(self.request, 'Нет слов для тренировки!')
            return self.get(self.request, *self.args, **self.kwargs)

        response = super().form_valid(form)

        training = form.instance
        for w in words:
            models.TrainingWord.objects.create(training=training, word=w)

        return response
