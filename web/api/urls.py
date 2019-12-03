from django.urls import path

from . import views

urlpatterns = [
    path('project-list', views.list, name='project-list'),
]