#!/bin/sh

if [ "1" = "1" ]
then
  python manage.py makemigrations user
  python manage.py migrate user
  python manage.py makemigrations home
  python manage.py migrate home
  python manage.py makemigrations
  python manage.py migrate

fi

if [ "$RTE" = "dev" ];
then
  export DJANGO_SUPERUSER_USERNAME
  export DJANGO_SUPERUSER_EMAIL
  export DJANGO_SUPERUSER_PASSWORD
  python manage.py createsuperuser --noinput
fi

if [ "1" = "1" ];
then
  echo "RUN CUSTOM COMMAND"
  python manage.py createpages
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
#python manage.py runserver 0.0.0.0:8000 &
#    pid=$!
#
#while true; do
#    inotifywait -e modify -r --exclude 'media' /usr/src/wagtailsite/
#    kill $pid
#    python manage.py runserver 0.0.0.0:8000 &
#    pid=$!
#done

exec "$@"
