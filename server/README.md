# Instructions

## Install Docker
## Install docker-compose


## Build the project:

`docker-compose build`

Open a terminal in this directory.

`docker-compose up db`

Running this it will not start the web server, but that's fine.
Just Ctrl-C it when it's done initializing.
This first time is just to create the db container and get it ready for the migrate
command:

`docker-compose run --rm web python manage.py migrate`

This creates the databases. (Sometimes this command fails the first time)

Change the permissions to `.` so that you own everything: `sudo chown -R $USER .`


## Start it running:

`docker-compose up`


## Shortcuts:

Consider adding an alias fserver="docker-compose run --rm web"

Consider adding an alias shell_plus="docker-compose run --rm web python manage.py shell_plus"

