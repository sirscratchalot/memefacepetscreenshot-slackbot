import os
import logging
import mimetypes
import slack
import json
from slack import RTMClient
import ssl as ssl_lib
import certifi
from typing import Callable

__messagelambda: Callable[[slack.WebClient,
                          str,
                          str,
                          dict
                           ], None] = None


def init_rtm(slack_token: str,
             messagelambda: Callable[[slack.WebClient,
                                     str,
                                     str,
                                     dict,
                                      ], None]):
    """Init the slack monitor and define the callback for events,
can be upgraded to dict for the future using a dict of callables"""
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    global __messagelambda
    __messagelambda = messagelambda
    print(__messagelambda)
    rtm_client.start()


@slack.RTMClient.run_on(event="message")
def message(**payload):
    """If in the list of monitored channels.
    """
    data = payload["data"]
    web_client: slack.WebClient = payload["web_client"]
    channel_id: str = data.get("channel")
    user_id: str = data.get("user")
    global __messagelambda
    __messagelambda(web_client, channel_id, user_id, data)

#    print("Message on channel:", channel_id, " : ", text, " :", data)

