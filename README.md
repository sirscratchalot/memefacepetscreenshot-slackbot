# MemeBot 2000

## Function

- This program uses a pretrained model to qualify images posted into Slack into one of four class.
- The program can also be used as a web-service taking an argument of a path or URL and identifying that image.

- Meme
- Faces
- Pets
- Screenshot

## Slack integration
From the repository folder:
- Install requirements using pip: "pip3 install -r requirements.txt"
- Create a slack app and bot token on `api.slack.com`, install the app to your workspace and invite the bot to any channel you wish to monitor.
- Set a valid slack-token in 'SLACK_BOT_TOKEN' environment variable i.e. on Linux: `export SLACK_BOT_TOKEN=XXXXXXXXX`
- Launch using 'python3 slackapp.py'
- Post an image url to any slack-channel where the bot is invited to trigger identification, or upload an image file.

## As a webservice
From the repository folder:
- Install requirements using pip: "pip3 install -r requirements.txt"
- Start flask using: `python3 -m flask run`
- Post an image local path or url (only https://) to localhost:5000/check_image?target=https://image.com/image.png

## Background

- At one point the developer needed to clean my pictures folder from memes and screenshots, accumulated over 20 years or more.
- To achieve this FastAI was used to train a simple Neural Network for vision and let it qualify images as memes or screenshots.
- Since memes are (typically) pictures of people or animals the network was also trained to recognize faces and pets with no memes.
-
