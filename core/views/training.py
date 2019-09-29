import random
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now

from django.views.generic import TemplateView, CreateView
from core import models
from core import consts


class Create(CreateView):
    template_name = 'core/object_create.html'
    model = models.Training
    fields = ('language', 'sections', 'direction',  'mode', )
    success_url = reverse_lazy('core:index')

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

        if self.request.GET.get('language'):
            initial['language'] = models.Language.objects.get(id=self.request.GET['language'])

        if self.request.GET.get('sections'):
            initial['sections'] = models.Section.objects.get(id__in=self.request.GET.getlist('sections'))

        return initial

    def form_valid(self, form):
        words = models.Word.objects.filter(
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
        for word in words:
            t_w = models.TrainingWord.objects.create(training=training, word=word)

            all_options = [w for w in words if w != word]
            random.shuffle(all_options)

            answer_options = all_options[:4]
            answer_options.append(word)
            random.shuffle(answer_options)

            t_w.answer_options.add(*answer_options)

        return response


class Process(TemplateView):
    template_name = 'core/training/process.html'

    def get_object(self):
        return models.Training.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        training = self.get_object()
        current_word = training.training_words.filter(answer_dt__isnull=True).last()

        c['object'] = training
        c['answered'] = training.training_words.filter(answer_dt__isnull=False).count()
        c['total'] = training.training_words.count()

        if training.direction == consts.DIRECTION_TO_RUS:
            c['question'] = current_word.word.name
            c['answers'] = [w.translation for w in current_word.answer_options.all()]
        else:
            c['question'] = current_word.word.translation
            c['answers'] = [w.name for w in current_word.answer_options.all()]

        return c

    def post(self, request, *args, **kwargs):
        c = self.get_context_data()
        training = self.get_object()
        current_word = training.training_words.filter(answer_dt__isnull=True).last()
        answer = self.request.POST['answer']

        current_word.answer = answer
        current_word.answer_dt = now()

        if training.direction == consts.DIRECTION_TO_RUS:
            right_answer = current_word.word.translation
        else:
            right_answer = current_word.word.name
        current_word.is_right = right_answer == answer
        current_word.save()

        if current_word.is_right:
            messages.success(request, f'{c["question"]} - "{answer}". Правильно.')
        else:
            messages.error(
                request, f'"{answer}" - не правильно. Правильный ответ для "{c["question"]}" - "{right_answer}".')

        if training.training_words.filter(answer_dt__isnull=True).exists():
            return redirect(reverse('core:training_process', kwargs={'pk': training.pk}))
        else:
            right_count = training.training_words.filter(is_right=True).count()
            wrong_count = training.training_words.filter(is_right=False).count()
            messages.info(
                request, f'Тренировка завершена! Правильных ответов {right_count}. Не правильных - {wrong_count}')
            return redirect(reverse('core:index'))


class Cancel(TemplateView):
    template_name = 'core/training/cancel.html'

    def get_object(self):
        return models.Training.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        training = self.get_object()
        c['object'] = training
        return c

    def post(self, request, *args, **kwargs):
        training = self.get_object()
        training.canceled = now()
        training.save()
        messages.warning(request, 'Тренировка была отменена')
        return redirect(reverse('core:index'))
