import slack
import mimetypes
from config import Config
import app.slackmonitor
import json
import os
import requests
from app.slackutil import MessageBuilder
from app.inference import LearnerInferer

__learner: LearnerInferer = None
__headers: dict = None
__placeholder = "https://2gony02cb42x1yqacu25se4a1049-wpengine.netdna-ssl.com/wp-content/uploads/2017/10/Etimo-blue-transparent-200x81-2.png"


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
        infered = {}
        message = {}
        try:
            if image.startswith("https://files.slack"):
                infered = __learner.infer(image, __headers)
                message = MessageBuilder().buildMessage(
                                           channel, __placeholder, infered)
            else:
                infered = __learner.infer(image)
                message = MessageBuilder().buildMessage(
                                           channel, image, infered)
            client.chat_postMessage(**message)
        except Exception as e:
            print(e)
            print("Exception while checking image...")
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


