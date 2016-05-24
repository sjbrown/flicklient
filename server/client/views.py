# client.views

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

def index(request):

    prs = PhotoRaw.objects.order_by("_created")
    photos = []
    for pr in prs:
        photo = Photo()
        photo.from_raw(pr)
        photos.append(photo)

    faves = []
    if request.user.is_authenticated():
        faves = request.user.photo_set.order_by('_created')[:50]
        faves = [x.link for x in faves]

    return makoify(request, 'index', **{
        'user': request.user,
        'photos': photos,
        'faves': faves,
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
            print 'valid log in'
            print 'uname', form.cleaned_data.get('username')
            print 'pword', form.cleaned_data.get('password')
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            login(request, user)
            return HttpResponseRedirect(reverse('client:index'))
        print 'NOT valid log in'

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
        print 'Link is', link

        try:
            pr = PhotoRaw.objects.get(link=link)
            print 'pr is', pr
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



