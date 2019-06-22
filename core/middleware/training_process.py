from django.shortcuts import redirect
from django.urls import reverse

from core import models
import core.views.training


class TrainingProcessMiddleware(object):
    """Мидлвара редиректит на неоконченную тренировку"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        if view_func.view_class in (core.views.training.Process, core.views.training.Cancel):
            return None

        uncompleted_training = models.Training.objects.filter(
            user=request.user,
            training_words__answer_dt__isnull=True,
            canceled__isnull=True,
        )
        if uncompleted_training.exists():
            training = uncompleted_training[0]
            return redirect(reverse('core:training_process', kwargs={'pk': training.pk}))

        return None
