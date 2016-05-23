#! /usr/bin/env python2.7

import json
import string
import datetime
import functools
import logging

from django.db import models
from django.utils import timezone
from django_extensions.db.fields import CreationDateTimeField
from django.db.models.signals import post_init, pre_save, post_save

from client.lazyjason import LazyJason, post_init_for_lazies, pre_save_for_lazies, post_save_for_lazies

# DEBUG value: 1 minute, production value: 1 hour
EXPIRY_AGE = datetime.timedelta(minutes=2)
#EXPIRY_AGE = datetime.timedelta(hours=1)

def younger_than_one_day_ago(model_obj):
    age = datetime.datetime.now() - model_obj._created
    return age < datetime.timedelta(days=1)

def defang_user_input(s):
    chars = []
    for c in s:
        if c in ' ' + string.letters + string.digits + '!@#$%^*()_-+=?/.,[]{}\|':
            chars.append(c)
    return ''.join(chars)

class Photo(models.Model, LazyJason):
    _created = CreationDateTimeField()
    db_attrs = models.CharField(default='{}', max_length=100*1024)
    _lazy_defaults = dict(
        title = "",
        link = "",
        media = "",
    )

    def __unicode__(self):
        return self.link

    def from_raw(self, photo_raw):
        self.link = photo_raw.link
        d = json.loads(photo_raw.text)
        self.media = d['media']['m']
        for key in ['title', 'date_taken', 'description', 'author', 'tags']:
            try:
                setattr(self, key, defang_user_input(d[key]))
            except Exception as e:
                logging.exception(e)

    @property
    def metadata(self):
        mdata = {}
        for key in ['link', 'title', 'date_taken', 'description', 'author', 'tags']:
            mdata[key] = getattr(self, key)
        return mdata


class PhotoRaw(models.Model):
    _created = CreationDateTimeField()
    text = models.CharField(max_length=10*1024)
    link = models.CharField(max_length=1024, unique=True)

    @classmethod
    def expire_old(cls):
        PhotoRaw.objects.filter(_created__lte =
            timezone.now() - EXPIRY_AGE
            ).delete()



for val in locals().values():
    if hasattr(val, '__bases__'):
        bases = val.__bases__
        if models.Model in bases and LazyJason in bases:
            post_init.connect(post_init_for_lazies, val)
            pre_save.connect(pre_save_for_lazies, val)
            post_save.connect(post_save_for_lazies, val)


