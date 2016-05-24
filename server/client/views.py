# client.views

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import mako
from mako.template import Template
from mako.lookup import TemplateLookup

from client.models import PhotoRaw, Photo


mplates = TemplateLookup(directories=['client/templates/client'])

def _date_to_str(date):
    return date.isoformat()

def _str_to_date(dstr):
    return datetime.strptime(dstr, "%Y-%m-%dT%H:%M:%S.%f")

def index(request):

    if 'last_seen' in request.session and 'startover' not in request.GET:
        only_show_after = _str_to_date(request.session['last_seen'])
        prs = PhotoRaw.objects.filter(_created__gt=only_show_after).order_by("_created")
    else:
        prs = PhotoRaw.objects.order_by("_created")

    photos = []
    for pr in prs[:3]:
        photo = Photo()
        photo.from_raw(pr)
        photos.append(photo)

    # We need to keep track of the last we've seen and whether we should
    # show the "Next..." link at the bottom of the HTML page
    at_the_end = False
    if photos:
        # pr is the last one from falling off the above loop
        request.session['last_seen'] = _date_to_str(pr._created)
        if pr == prs.last():
            at_the_end = True
        else:
            at_the_end = False

    faves = []
    if request.user.is_authenticated():
        faves = request.user.photo_set.order_by('_created').reverse()[:50]
        faves = [x.link for x in faves]

    return makoify(request, 'index', **{
        'user': request.user,
        'photos': photos,
        'faves': faves,
        'at_the_end': at_the_end,
        'messages': messages.get_messages(request),
    })


def sign_up(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('client:index'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password1'))
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))

    else:
        form = UserCreationForm()

    return render(request, 'client/sign_up.html',
                  context = { 'form': form, })

def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('client:index'))

def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('client:index'))

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))

    else:
        form = AuthenticationForm()

    return render(request, 'client/log_in.html',
                  context = { 'form': form, })




@login_required
def favourite(request):
    def validate(link_input):
        # TODO: do real validation
        return link_input

    if request.method == 'POST':
        link = validate(request.POST['link'])

        try:
            pr = PhotoRaw.objects.get(link=link)
            photo = Photo()
            photo.from_raw(pr)
            photo.owner = request.user
            photo.save()
            messages.info(request, 'Added Favourite.')

        except PhotoRaw.DoesNotExist:
            messages.error(request, 'Expired PhotoRaw.')

    return HttpResponseRedirect(reverse('client:index'))


@login_required
def unfavourite(request):
    def validate(link_input):
        # TODO: do real validation
        return link_input

    if request.method == 'POST':
        link = validate(request.POST['link'])

        try:
            faves = request.user.photo_set.all()
            for fave in faves:
                if fave.link == link:
                    fave.delete()
            messages.info(request, 'Removed Favourite.')

        except PhotoRaw.DoesNotExist:
            messages.error(request, 'Expired PhotoRaw.')

    return HttpResponseRedirect(reverse('client:index'))


@login_required
def show_faves(request):
    faves = request.user.photo_set.order_by('_created')
    photos = faves
    faves = [x.link for x in faves]

    return makoify(request, 'index', **{
        'user': request.user,
        'photos': photos,
        'faves': faves,
        'at_the_end': True,
        'messages': messages.get_messages(request),
    })


# -- helper functions

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



