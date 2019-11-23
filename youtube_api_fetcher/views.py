from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from youtube_api_fetcher.cron import fetch_from_youtube

from .models import Video

from background_task.models import Task

def cron(request):
    # clear previous tasks
    Task.objects.all().delete()
    fetch_from_youtube(repeat = 30)
    return HttpResponse("Cron Job Started")

def index(request):
    return HttpResponse("Project Started")
