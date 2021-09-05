from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core import models


class List(ListView):
    template_name = 'core/object_list.html'
    model = models.Word

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class Detail(DetailView):
    template_name = 'core/word/detail.html'
    model = models.Word


class Create(CreateView):
    template_name = 'core/word/create.html'
    model = models.Word
    fields = ('name', 'translation', 'transcription', 'sections', 'language', )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        # если такое слово в базе уже есть, то используем его
        word_qs = self.model.objects.filter(
            user=self.request.user,
            language=form.cleaned_data['language'],
            name=form.cleaned_data['name'],
        )
        if word_qs:
            # разделы объединим с предыдущими разделами слова
            form.cleaned_data['sections'] = list(form.cleaned_data['sections']) + list(word_qs[0].sections.all())
            form.instance = word_qs[0]
            # остальные поля обновим из текущей формы
            form.instance.translation = form.cleaned_data['translation']
            form.instance.transcription = form.cleaned_data['transcription']

        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get('section'):
            section = models.Section.objects.get(id=self.request.GET['section'])
            initial['sections'] = [section.pk]
            if section.words.exists():
                initial['language'] = section.words.last().language
        return initial

    def get_success_url(self):
        if self.request.GET.get('section'):
            return reverse('core:section_detail', kwargs={'pk': self.request.GET['section']})
        return reverse('core:word_list')


class Update(UpdateView):
    template_name = 'core/object_update.html'
    model = models.Word
    fields = ('name', 'translation', 'transcription', 'sections', 'language', )

    def get_success_url(self):
        return reverse('core:word_detail', kwargs={'pk': self.kwargs['pk']})


class Delete(DeleteView):
    template_name = 'core/object_delete.html'
    model = models.Word
    fields = ('name', )
    success_url = reverse_lazy('core:word_list')
