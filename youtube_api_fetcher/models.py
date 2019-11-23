from django.db import models

class Video(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=30)
    channelTitle = models.CharField(max_length=50)
    publishedAt = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return "id: {} , title: {}".format(self.id, self.title)
