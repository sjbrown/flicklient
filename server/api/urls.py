from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^v1/(?P<username>[^/]+)/favourites/?$',
        views.user_favourites, name='user_favourites'),

]

