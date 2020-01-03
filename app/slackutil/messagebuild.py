from collections import OrderedDict


class MessageBuilder:

    def buildMessage(self, channel, class_name,
                     image_url, losses: OrderedDict):
        print(channel,class_name,image_url,losses)
        return self.__BASE_MESSAGE.format(
                                   channel,
                                   class_name,
                                   image_url,
                                   self.buildList(losses))

    def buildList(self, losses: OrderedDict):
        del losses["predicted_class"]
        list_string = "\\n".join([
            "\n{}. {}: {}%".format(i, tup[0], tup[1])
            for i, tup in enumerate(losses.items())])
        return list_string

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
                                        "meme",
                                        "https://far-away.com/1.png",
                                        infered_dict))

