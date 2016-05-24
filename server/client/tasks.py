from __future__ import absolute_import
from celery import Celery

import json
import logging
import requests
from client import flickr_json_feed
from client.models import FeedPhoto

FLICKR_URL = 'https://api.flickr.com/services/feeds/photos_public.gne?format=json'

BROKER_URL = 'django://'
#BROKER_URL = 'redis://localhost' #TODO

app = Celery('tasks', broker=BROKER_URL)
app.conf.update(
     CELERY_ACCEPT_CONTENT = ['json'],
     CELERY_TASK_SERIALIZER = 'json',
     CELERY_RESULT_SERIALIZER = 'json',
)


def populate(photo_dicts):
    # They've gone through their lives as both JSON and Python dicts,
    # so with a little more validation they're ready to store in the database
    for d in photo_dicts:
        try:
            # One last validation: check for d['media']['m']
            d['media']['m'] # Throws KeyError if it doesn't exist

            pr = FeedPhoto(text=json.dumps(d), link=d['link'])

            # This will throw an exception if the link isn't unique
            pr.save()

        except Exception as e:
            # Probably not unique
            logging.exception(e)


@app.task
def download_feed():
    photo_dicts = {}

    response = requests.get(FLICKR_URL)

    try:
        photo_dicts = flickr_json_feed.response_to_photo_dicts(response)
        populate(photo_dicts)
        FeedPhoto.expire_old()
        countdown = 60

    except (Exception, KeyError) as e:
        logging.exception(e)
        countdown = 5

    download_feed.apply_async(
        expires=90,
        countdown=countdown,
    )

    return photo_dicts


download_feed.apply_async(
    expires=90,
    countdown=5
)
