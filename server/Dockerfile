from python:2.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /projects
WORKDIR /projects

RUN pip install Django
RUN pip install djangorestframework
RUN pip install psycopg2
RUN pip install Mako
RUN pip install ipython
RUN pip install django-extensions
RUN pip install django-celery
RUN pip install django-kombu
RUN pip install -U celery
RUN pip install requests
ADD . /projects/

ENV SHELL_PLUS="ipython"
