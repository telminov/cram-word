from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from core import models


class List(ListView):
    template_name = 'core/object_list.html'
    model = models.Section


class Detail(DetailView):
    template_name = 'core/object_detail.html'
    model = models.Section


class Create(CreateView):
    template_name = 'core/object_create.html'
    model = models.Section
    fields = ('name', )
    success_url = reverse_lazy('core:section_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.instance.user = self.request.user
        return form


class Update(UpdateView):
    template_name = 'core/object_update.html'
    model = models.Section
    fields = ('name', )
    success_url = reverse_lazy('core:section_list')


class Delete(DeleteView):
    template_name = 'core/object_delete.html'
    model = models.Section
    fields = ('name', )
    success_url = reverse_lazy('core:section_list')
