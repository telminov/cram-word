from django.urls import reverse

from django.views.generic import TemplateView


class IndexView(TemplateView):
    title = 'Главная'
    template_name = 'core/index.html'

    def get_breadcrumbs(self):
        return [
            ('Главная', reverse('core:index')),
        ]
