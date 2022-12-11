#!/bin/bash
#Prepare for dango
python3 manage.py migrate

#Start uwsgi
uwsgi --ini uwsgi.ini

