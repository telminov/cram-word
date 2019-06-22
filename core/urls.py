from django.urls import path
from core.views import index
from core.views import section

app_name = 'core'

urlpatterns = [
    path('', index.Index.as_view(), name='index'),

    path('section/', section.List.as_view(), name='section_list'),
    path('section/create/', section.Create.as_view(), name='section_create'),
    path('section/<int:pk>/', section.Detail.as_view(), name='section_detail'),
    path('section/<int:pk>/update/', section.Update.as_view(), name='section_update'),
    path('section/<int:pk>/delete/', section.Delete.as_view(), name='section_delete'),

]

