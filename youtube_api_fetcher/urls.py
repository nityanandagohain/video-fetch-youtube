from django.urls import path

from . import views

urlpatterns = [
    path('cron', views.cron, name='cron'),
    path('', views.index, name='index'),
]