FROM ubuntu:14.04
MAINTAINER Spencer Smith <robertspencersmith@gmail.com>

ENV APPDIR /app
WORKDIR $APPDIR

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install Flask gunicorn
ADD app.py /app/app.py
EXPOSE 5000
