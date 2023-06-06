#!/bin/sh

PIDFILE=/var/www/memorandum/run/memorandum.pid

case $1 in 
start)
NAME="memorandum"
DJANGODIR=/var/www/memorandum/
SOCKFILE=/var/www/memorandum/run/gunicorn.sock
USER=root
GROUP=root
NUM_WORKERS=2
DJANGO_SETTINGS_MODULE=Memorand.settings
DJANGO_WSGI_MODULE=Memorand.wsgi
echo "Starting $NAME as `whoami`"
cd $DJANGODIR
source /var/www/memorandum/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
# Start your Django Unicorn# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
/var/www/memorandum/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
--name $NAME \
--workers $NUM_WORKERS \
--user=$USER --group=$GROUP \
--bind=unix:$SOCKFILE \
--log-level=debug \
--log-file=- \
--pid=$PIDFILE &
;;
stop)
kill -9 $(cat $PIDFILE)
rm $PIDFILE
;;
restart)
/etc/init.d/memorandum.sh stop
/etc/init.d/memorandum.sh start
;;

esac

exit 0
