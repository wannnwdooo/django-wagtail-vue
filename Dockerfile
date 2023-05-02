FROM python:3.8.1-slim-buster

RUN useradd wagtail

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat \
 && rm -rf /var/lib/apt/lists/*
#RUN apt-get update && apt-get install -y inotify-tools
#RUN pip install watchdog
RUN pip install "gunicorn==20.0.4"

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /usr/src/wagtailsite

RUN chown wagtail:wagtail /usr/src/wagtailsite

COPY --chown=wagtail:wagtail . .

USER wagtail

RUN python manage.py collectstatic --noinput --clear
CMD set -xe; python manage.py migrate --noinput; gunicorn wagtailsite.wsgi:application
RUN sed -i 's/\r$//g' entrypoint.sh

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/usr/src/wagtailsite/entrypoint.sh"]
