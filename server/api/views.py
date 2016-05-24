# api.views

import json

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from client.models import Photo



def user_favourites(request, **kwargs):

    u = get_object_or_404(User, username=kwargs['username'])

    faves = u.photo_set.all()
    faves = {
        'username': u.username,
        'favourites': [x.metadata for x in faves]
    }
    return JsonResponse(faves)

