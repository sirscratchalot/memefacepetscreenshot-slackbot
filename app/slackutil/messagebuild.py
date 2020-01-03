from collections import OrderedDict
import json

class MessageBuilder:

    def buildMessage(self, channel,
                     image_url, losses: OrderedDict):
        return json.loads(self.__BASE_MESSAGE.format(
                                   channel,
                                   losses.get("predicted_class"),
                                   image_url,
                                   self.buildList(losses)))

    def buildList(self, losses: OrderedDict):
        list_string = "\\n".join([
            "{}. {}: {}%".format(i, tup[0], tup[1])
            for i, tup in enumerate(losses.items()) if i > 0])
        return "\\n"+list_string

    __BASE_MESSAGE = """
    {{
        "channel": "{}",
        "username": "MemeIdentifierBot",
        "icon_emoji": ":cat:",
            "blocks": [
                {{
                    "type": "section",
                    "text": {{
                        "type": "mrkdwn",
                        "text": "I think this is a: {}"
                    }},
                            "accessory":{{
                    "type": "image",
                    "image_url": "{}",
                    "alt_text": "The image analyzed"
                }}
                }},
                {{
                    "type": "divider"
                }},
                {{
                    "type": "section",
                    "text": {{
                        "type": "mrkdwn",
                        "text": "This is how sure I was:{}"
                    }}
                }}

            ]
    }}
    """


if __name__ == "__main__":
    infered_dict = {"predicted_class": "meme",
                    "meme": 100.0, "faces": 0.0,
                    "pet": 0.0, "screenshot": 0.0}
    infered_dict = OrderedDict(infered_dict.items())

    print(MessageBuilder().buildMessage("Channel1",
                                        "https://far-away.com/1.png",
                                        infered_dict))

