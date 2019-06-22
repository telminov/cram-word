from django.urls import path
from core.views import index
from core.views import section
from core.views import word

app_name = 'core'

urlpatterns = [
    path('', index.Index.as_view(), name='index'),

    path('section/', section.List.as_view(), name='section_list'),
    path('section/create/', section.Create.as_view(), name='section_create'),
    path('section/<int:pk>/', section.Detail.as_view(), name='section_detail'),
    path('section/<int:pk>/update/', section.Update.as_view(), name='section_update'),
    path('section/<int:pk>/delete/', section.Delete.as_view(), name='section_delete'),

    path('word/', word.List.as_view(), name='word_list'),
    path('word/create/', word.Create.as_view(), name='word_create'),
    path('word/<int:pk>/', word.Detail.as_view(), name='word_detail'),
    path('word/<int:pk>/update/', word.Update.as_view(), name='word_update'),
    path('word/<int:pk>/delete/', word.Delete.as_view(), name='word_delete'),

]

