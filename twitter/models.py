from django.db import models


class TwitterHandle(models.Model):
    twitter_handle = models.CharField(max_length=200)

    def __str__(self):
        return self.twitter_handle

class TwitterMonthly(models.Model):
    since_date = models.DateTimeField
