from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from format import format_dates, format_options
from query_tweets import query
from django.views.decorators.csrf import csrf_exempt
from initial_login import create_profile
import tweepy


def begin_auth(request):

    callback_url = request.build_absolute_uri('login/authenticated/')
    auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET, callback=callback_url)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print "Failed to get request token"

    request.session['request_token'] = auth.request_token
    return HttpResponseRedirect(redirect_url)


def twittr_authenticated(request):

    verifier = request.GET.get('oauth_verifier')
    auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
    auth.request_token = request.session['request_token']

    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print "Failed to get access token"

    api = tweepy.API(auth)

    # Check if the user already exists
    try:
        User.objects.get(username=api.me().screen_name)

    # First time user create a new profile and save their info
    except User.DoesNotExist:
        create_profile(auth)

    user = authenticate(username=api.me().screen_name, password=auth.access_token_secret)

    # Log them in and redirect to the main page
    login(request, user)
    redirect_url = "/twittr/accounts/%s" % user.username

    return HttpResponseRedirect(redirect_url)


@login_required(login_url='/twittr/login/')
def search_form(request, username):
    profile = request.user.twitterprofile
    auth = tweepy.OAuthHandler(settings.TWITTER_TOKEN, settings.TWITTER_SECRET)
    auth.set_access_token(profile.oauth_token, profile.oauth_secret)
    api = tweepy.API(auth)

    latest_tweets = tweepy.Cursor(api.user_timeline).items(20)
    return render_to_response('search_form.html', {'profile': request.user.twitterprofile, 'tweets': latest_tweets})


@csrf_exempt
def search_submit(request, username):

    # Grab the data POST using ajax
    user_query = request.POST.get('search')
    selected = request.POST.getlist('selected[]')
    dates = request.POST.getlist('dates[]')

    # Clean things up
    dates = format_dates(dates)
    options = format_options(selected)
    user_query = unicode(user_query)

    tweets = query(request.user.twitterprofile, user_query, dates, options)
    return render_to_response('tweets.html', {'profile': request.user.twitterprofile, 'tweets': tweets})


@login_required(login_url='/twittr/login/')
def twittr_logout(request):
    logout(request)
    # Should redirect to erasr's homepage
    return HttpResponseRedirect('/')
