from datetime import datetime
from django.utils import timezone
from django.db.models import Q


def query(profile, user_query, selected_dates, options):

    start_date, end_date = grab_dates(selected_dates)

    # Tweets that contain the query text within the selected dates
    results = profile.tweets.filter(
        text__icontains=user_query,
        created__range=(start_date, end_date)
    )

    # Get rid of the text only tweets if user deselects 'All'
    if not options['all']:
        results = results.filter(
            Q(is_image=True) | Q(is_retweet=True) |
            Q(is_quote=True) | Q(is_video=True)
        )

    # Exclude anything options the user set to false
    if not options['images']:
        results = results.exclude(is_image=True)

    if not options['retweets']:
        results = results.exclude(is_retweet=True)

    if not options['quotes']:
        results = results.exclude(is_quote=True)

    if not options['media']:
        results = results.exclude(is_video=True)

    # Return in chronological order by most recent
    return list(results.order_by('created').reverse())


def erase(profile, api, tweet_ids):

    # Remove from twitter
    (api.destroy_status(t_id) for t_id in tweet_ids)

    # Remove from profile/db
    profile.tweets.filter(id__in=tweet_ids).delete()


# Helper Function
def grab_dates(selected_dates):
    # Grab the info user entered into the drop-down. Initial format ex: 1, 1, 2016, 12, 31, 2016.
    selected_start = str(selected_dates[0]) + " " + str(selected_dates[1]) + " " + str(selected_dates[2])
    selected_end = str(selected_dates[3]) + " " + str(selected_dates[4]) + " " + str(selected_dates[5])

    # Convert to datetime objects
    start = datetime.strptime(selected_start, "%m %d %Y")
    end = datetime.strptime(selected_end, "%m %d %Y")

    #
    start = timezone.make_aware(start, timezone.get_current_timezone())
    end = timezone.make_aware(end, timezone.get_current_timezone())

    return start, end
