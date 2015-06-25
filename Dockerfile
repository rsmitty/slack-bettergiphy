FROM ubuntu:14.04
MAINTAINER Spencer Smith <robertspencersmith@gmail.com>

ENV APPDIR /app
WORKDIR $APPDIR

RUN apt-get update
RUN apt-get install -y python-flask
ADD giphybot.py /app/giphybot.py
EXPOSE 5000
CMD python giphybot.py

