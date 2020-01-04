FROM ubuntu:latest
MAINTAINER sirscratchalot "erik.malm@etimo.se"
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN mkdir -p /opt/memebot
ADD requirements.txt /opt/memebot
ADD *.py /opt/memebot/
ADD app /opt/memebot/
ADD models /opt/memebot/
RUN  pip3 install --upgrade pip && pip install -r /opt/memebot/requirements.txt --no-cache-dir
RUN useradd memebot && chown -R memebot:memebot /opt/memebot
WORKDIR /opt/memebot
ENV SLACK_BOT_TOKEN $SLACK_BOT_TOKEN
CMD ["python", "/opt/memebot/slackapp.py"]

