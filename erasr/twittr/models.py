from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tweet(models.Model):
    temp = models.CharField(max_length=100, primary_key=True, unique=True, default=0)
    text = models.CharField(max_length=500)
    created = models.DateTimeField()
    is_retweet = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)
    is_quote = models.BooleanField(default=False)
    is_image = models.BooleanField(default=False)
    is_video = models.BooleanField(default=False)
    media_url = models.CharField(max_length=500)


class TwitterProfile(models.Model):
    user = models.OneToOneField(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    profile_pic = models.CharField(max_length=200, default="")
    username = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    followers = models.PositiveIntegerField(default=0)
    following = models.PositiveIntegerField(default=0)
    tweet_count = models.PositiveIntegerField(default=0)
    tweets = models.ManyToManyField(Tweet)
