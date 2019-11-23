from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from background_task.models import Task

from .cron import fetch_from_youtube
from .models import Video

# clear previous tasks
Task.objects.all().delete()

def cron(request):
    # clear previous tasks
    if Task.objects.count() > 0:
        Task.objects.all().delete()

    fetch_from_youtube(repeat = 30)
    return HttpResponse("<h1>Cron Job Started<h1>")

def index(request):
    # Getting all videos in descending order
    video_list = Video.objects.all().order_by('-publishedAt')
    page = request.GET.get('page', 1)

    # Pagination with 10 values per page
    paginator = Paginator(video_list, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    return render(request, 'index.html', { 'videos': videos })