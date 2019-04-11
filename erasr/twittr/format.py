import time
import datetime


__doc__ = """Convert the values read in from the html into something easier to work with"""


def format_time(tweets):
    for tweet in tweets:
        # Mon Jan 18 01:27:43 +0000 2016 --> January 18, 2016
        created_at = time.strptime(tweet.created_at, "%a %b %d %H:%M:%S +0000 %Y")
        formatted_tweet_time = time.strftime("%B %d, %Y", created_at)
        tweet.created_at = formatted_tweet_time


# Create a dictionary with all possible options and mark the ones selected as true
def format_options(selected):
    all_options = ["all", "mentions", "retweets", "quotes", "images", "media"]

    # Initial dictionary has all of the options set to false
    options = {o: False for o in all_options}

    for s in selected:
        options[s.strip().lower()] = True

    return options


def format_dates(dates):
    # If a month or day has not been selected then default to 1
    dates[0] = default_date(dates[0], 1)     # start month
    dates[1] = default_date(dates[1], 1)     # start day

    # Default value for the end date is the last day of the year
    dates[3] = default_date(dates[3], 12)    # end month
    dates[4] = default_date(dates[4], 30)    # end day

    # If a year has not been selected then default to 2006 and end on the last day of the current year
    dates[2] = default_date(dates[2], 2006)    # start year
    dates[5] = default_date(dates[5], datetime.datetime.now().year)    # end year

    return dates


# If the user left the field empty set it to a default value. Otherwise leave it alone
def default_date(date, default_val):
    if len(date) == 0 or "Select" in str(date):
        return default_val

    return date
