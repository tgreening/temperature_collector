from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<probe_name>[a-zA-Z]+)/reading/', views.reading, name='reading'),
    url(r'^(?P<probe_name>[a-zA-Z]+)/latest/', views.latest, name='latest'),
    url(r'^(?P<probe_name>[a-zA-Z]+)/average/', views.average, name='average'),
    url(r'^ga/', views.ga, name='ga'),
    url(r'^slack/', views.slack, name='slack')
]
