from django.urls import path

from . import views

urlpatterns = [
    path('projects', views.projects, name='projects'),
    # path('spiders', views.spiders, name='spiders'),
    # path('all-spiders', views.all_spiders, name='all-spiders'),
    # path('crawl', views.crawl, name='crawl'),
    # path('stop', views.stop, name='stop'),
    # path('pause', views.pause, name='pause'),
    # path('unpause', views.unpause, name='unpause'),
    path('ping', views.ping, name='ping'),
]