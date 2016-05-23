# Instructions

(from https://docs.docker.com/compose/django/)

## Install Docker
## Install docker-compose


## Build the project:

`docker-compose build`

Open a terminal in this directory.

`docker-compose run --rm web python manage.py migrate`

This creates the databases.

Change the permissions to `.` so that you own everything: `sudo chown -R $USER .`


## Start it running:

`docker-compose up`


## Shortcuts:

Consider adding an alias fserver="docker-compose run --rm web"

Consider adding an alias shell_plus="docker-compose run --rm web python manage.py shell_plus"

