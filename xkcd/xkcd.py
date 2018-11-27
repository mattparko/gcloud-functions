# Google Cloud Function / Python 3.7 runtime

# Currently only supports Google Hangouts Chat (due to event type handling)

import requests
import random
import re
from flask import jsonify

BOTNAME = "xkcd-test"

def get_comic(comic_number):
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    r = requests.get("https://xkcd.com/{}/info.0.json".format(comic_number), headers=headers)
    comic = r.json()
    payload = {
        "cards": [{
            "header": {
                "title": comic["safe_title"],
                "subtitle": "xkcd.com/{}\n".format(comic["num"])
            },
            "sections": [{
                "widgets": [{
                    "image": {
                        "imageUrl": comic["img"],
                        "onClick": {
                            "openLink": {
                                "url": "https://xkcd.com/{}".format(comic["num"])
                            }
                        }
                    }},
                    {
                    "textParagraph": {
                        "text": "<br>(<i>alt-text</i>) {}".format(comic["alt"])
                    }
                }]
            }]
        }]
    }
    return jsonify(payload)

def get_random_comic():
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    r = requests.get("https://xkcd.com/info.0.json", headers=headers)
    latest = r.json()["num"]
    random_comic_number = random.choice(range(1,int(latest)))
    return get_comic(random_comic_number)

def get_help_text():
    help_text = """
Hi! I can help with all of your xkcd needs

Actions:
*Get the latest comic:* @{0} latest
*Get a random comic:* @{0} random
*Get a specific comic:* @{0} <number>
*Show this help message:* @{0} help
""".format(BOTNAME)
    return jsonify({"text": help_text})

def main(request):
    event_type = request.json["type"]
    if event_type == "MESSAGE":
        message = request.json["message"]["text"].split()
        # Remove @BOTNAME from message to handle both group chats and DMs
        if message[0] == "@{}".format(BOTNAME):
            message.pop(0)
        if not message or message[0].lower() == "latest":
            response = get_comic("")
        elif message[0].lower() == "random":
            response = get_random_comic()
        elif re.match(r"[0-9]+", message[0]):
            response = get_comic(message[0])
        else:
            response =  get_help_text()
    elif event_type == "ADDED_TO_SPACE":
        response = get_help_text()
    elif event_type == "REMOVED_FROM_SPACE":
        response = None

    return response
