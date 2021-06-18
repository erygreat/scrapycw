from django.urls import path

from . import views

urlpatterns = [
    path('project-list', views.project_list, name='project-list'),
    path('spider-list', views.spider_list, name='spider-list'),
    path('crawl', views.crawl, name='crawl'),
    path('stop', views.stop, name='stop'),
    path('pause', views.pause, name='pause'),
    path('unpause', views.unpause, name='unpause'),
    path('ping', views.ping, name='ping'),
]