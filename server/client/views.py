# client.views

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf

import mako
from mako.template import Template
from mako.lookup import TemplateLookup

from client.models import PhotoRaw, Photo


mplates = TemplateLookup(directories=['client/templates/client'])

def index(request):
    print '----index'

    prs = PhotoRaw.objects.order_by("_created")
    photos = []
    for pr in prs:
        photo = Photo()
        photo.from_raw(pr)
        photos.append(photo)

    return makoify(request, 'index', **{
        'user': {'a':12},
        'pics': [photos[0].media, photos[1].media,],
        'metadata': [photos[0].metadata, photos[1].metadata],
    })


def make_url(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)

def make_csrf(request):
    return '<input type="hidden" name="csrfmiddlewaretoken" value="%s" />' %\
        csrf(request)["csrf_token"]

def makoify(request, template_prefix, **kw):
    template = mplates.get_template(template_prefix +'.mako')
    try:
        result = template.render(
            csrf=make_csrf(request),
            make_url=make_url,
            lookup=mplates,
            **kw
        )
    except:
        result = mako.exceptions.html_error_template().render()
    return HttpResponse(result)



