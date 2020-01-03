import os

class Config(object):

    #Flask config is used around the app for a lot of flask stuff
    SECRET_KEY= os.environ.get("SECRET_KEY") or "This_is_top_secret!"

    #Config for slack integration
    SLACK_BOT_TOKEN= os.environ.get("SLACK_BOT_TOKEN") or "None"

    #Config for image inferer
    MODEL_PATH="models"
    MODEL_FILE="memepetfacescreen.pkl"
