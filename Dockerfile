FROM ubuntu:20.04
MAINTAINER sirscratchalot "erik.malm@etimo.se"
RUN apt-get update \
  && apt-get install -y  python3-dev python3-pillow python3-pip\
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN mkdir -p /opt/memebot
ADD requirements.txt /opt/memebot
RUN  pip3 install --upgrade pip && pip install -r /opt/memebot/requirements.txt --no-cache-dir
ADD *.py /opt/memebot/
ADD app /opt/memebot/app
ADD models /opt/memebot/models
RUN useradd memebot && chown -R memebot:memebot /opt/memebot
WORKDIR /opt/memebot
#This needs to be set for app to work
ARG bot_token=this-is-a-default-value
ENV SLACK_BOT_TOKEN $bot_token
RUN echo $SLACK_BOT_TOKEN
CMD ["/usr/bin/python3", "/opt/memebot/slackapp.py"]

