import slack
import mimetypes
from config import Config
import app.slackmonitor
import json
import os
import requests

from app.inference import LearnerInferer

__learner: LearnerInferer = None
__headers: dict = None


def getImage(data: dict):
    subtype: str = data.get("subtype")

    if subtype == "message_changed" and data.get("message") is not None:
        return getUrl(data.get("message"))
    else:
        return getFile(data)


def getUrl(data: dict):
    blocks = data.get("attachments")
    if blocks is None:
        return None
    for x in blocks:
        image = x.get("image_url")
        if image is None:
            return None
        return image
    return None


def getFile(data: dict):
    blocks = data.get("files")
    if blocks is None:
        return None
    for x in blocks:
        image = x.get("url_private_download")
        if image is None:
            return None
        return image
    return None


def handle_message(client: slack.WebClient,
                   channel: str, user: str, data: dict):
    image = getImage(data)
    if image is not None:
        mime, encoding = mimetypes.guess_type(image)
        print("I got a linked  image!; ",
              mime.startswith("image"),
              ": ", image)
        if image.startswith("https://files.slack"):
            print(__learner.infer(image, __headers))
        else:
            print(__learner.infer(image))

    else:
        print("I got an image with no message!: ", image)


def init():
    conf = Config()

    global __learner, __headers
    __learner = LearnerInferer(conf.MODEL_PATH, conf.MODEL_FILE)
    __headers = {"Authorization": "Bearer {}".format(conf.SLACK_BOT_TOKEN)}
    app.slackmonitor.init_rtm(conf.SLACK_BOT_TOKEN, handle_message)


if __name__ == "__main__":
    init()


