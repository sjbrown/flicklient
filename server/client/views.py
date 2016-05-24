# client.views

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

import mako
from mako.template import Template
from mako.lookup import TemplateLookup

from client.models import PhotoRaw, Photo


mplates = TemplateLookup(directories=['client/templates/client'])

def index(request):
    print '----index'
    print '----rq u', request.user

    prs = PhotoRaw.objects.order_by("_created")
    photos = []
    for pr in prs:
        photo = Photo()
        photo.from_raw(pr)
        photos.append(photo)

    return makoify(request, 'index', **{
        'user': request.user,
        'photos': photos,
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
        print 'HERE'
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



