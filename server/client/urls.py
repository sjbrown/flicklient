from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sign_up/?$', views.sign_up, name='sign_up'),
    url(r'^log_in/?$', views.log_in, name='log_in'),
    url(r'^log_out/?$', views.log_out, name='log_out'),
    url(r'^favourite/?$', views.favourite, name='favourite'),
    url(r'^unfavourite/?$', views.unfavourite, name='unfavourite'),
    url(r'^show_faves/?$', views.show_faves, name='show_faves'),

    url('', include('django.contrib.auth.urls')),

]

