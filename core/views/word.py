from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core import models


class List(ListView):
    template_name = 'core/object_list.html'
    model = models.Word


class Detail(DetailView):
    template_name = 'core/word/detail.html'
    model = models.Word


class Create(CreateView):
    template_name = 'core/object_create.html'
    model = models.Word
    fields = ('name', 'translation', 'transcription', 'sections', 'language', )
    success_url = reverse_lazy('core:word_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form

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
