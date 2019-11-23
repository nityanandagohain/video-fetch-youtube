import requests
import os
import json
from datetime import datetime, timezone
import dateutil.relativedelta
from background_task import background
from django.contrib.auth.models import User
from dateutil import parser


from .models import Video

@background(schedule=2)
def fetch_from_youtube():
    # get the current datetime
    local_time = datetime.now(timezone.utc).astimezone()
    time = local_time.isoformat()

    # send request to the youtube API
    url = "https://www.googleapis.com/youtube/v3/search"    
    querystring = {"key": os.environ.get("YOUTUBE_KEY"),"part":"snippet","type":"video","q":"football", "publishedAfter": time, "maxResults": 50}
    try:
        response = requests.request("GET", url, params=querystring)
        res = json.loads(response.text)
    except:
        print("Error while fetching from youtube API")

    # iterate though the results from the API
    for video in res["items"]:
        try:
            newvideo = Video.objects.get(id=video["id"]["videoId"])
            print("video: {} already present in Database".format(video["id"]["videoId"]))
        except (Video.DoesNotExist):
            newvideo = Video(id = video["id"]["videoId"], 
                            title = video["snippet"]["title"], 
                            publishedAt = parser.parse(video["snippet"]["publishedAt"]), 
                            description = video["snippet"]["description"], 
                            channelTitle= video["snippet"]["channelTitle"])
            newvideo.save()
            print("video: {} saved".format(video["id"]["videoId"]))