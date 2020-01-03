import os

class Config(object):
    #Flask config is used around the app for a lot of flask stuff
    SECRET_KEY= os.environ.get("SECRET_KEY") or "This_is_top_secret!"
    SLACK_KEY= os.environ.get("SLACK_KEY") or "None"
    MODEL_PATH="models"
    MODEL_FILE="memepetfacescreen.pkl"
