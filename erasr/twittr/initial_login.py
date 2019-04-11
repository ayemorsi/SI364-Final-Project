import tweepy
from models import TwitterProfile, Tweet
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction


def create_profile(auth):
    api = tweepy.API(auth)
    user = User.objects.create_user(username=api.me().screen_name, password=auth.access_token_secret)
    profile = TwitterProfile()
    profile.user = user
    profile.oauth_token = auth.access_token
    profile.oauth_secret = auth.access_token_secret
    profile.username = api.me().screen_name
    profile.name = api.me().name
    profile.following = api.me().friends_count
    profile.followers = api.me().followers_count
    profile.profile_pic = api.me().profile_image_url_https.replace('normal', '400x400')  # Hack for higher-res
    profile.tweet_count = api.me().statuses_count
    profile.save()

    load_tweets(profile, api)


@transaction.atomic
def load_tweets(profile, api):

    tweets = []
    for status in tweepy.Cursor(api.user_timeline).items():
        print str(status.id)
        tweet = Tweet(temp=str(status.id)[-9:])

        tweet.text = unicode(status.text)
        tweet.created = timezone.make_aware(status.created_at, timezone.get_current_timezone())
        tweet.is_retweet = status.retweeted
        tweet.retweet_count = status.retweet_count
        tweet.is_quote = status.is_quote_status

        if status.in_reply_to_status_id is not None:
            tweet.is_reply = True

        for media in status.entities.get("media", [{}]):
            if media.get("type", None):
                tweet.media_url = media.get('media_url')

                if 'video' in tweet.media_url:
                    tweet.is_video = True
                else:
                    tweet.is_image = True

        # tweets.append(tweet)
        tweet.save()
        profile.tweets.add(tweet)
    # profile.tweets.bulk_create(tweets)
    profile.save()


