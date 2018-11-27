# Google Cloud Function / Python 3.7 runtime

# Currently only supports Google Hangouts Chat (due to event type handling)

import requests
import random
import re
from flask import jsonify

BOTNAME = "xkcd"
HEADERS = {"Accept": "application/json", "Content-type": "application/json"}

def get_comic_text(comic_number=""):
    """ Fetches comic info and returns a formatted text-based response """
    r = requests.get("https://xkcd.com/{}/info.0.json".format(comic_number), headers=HEADERS)
    comic = r.json()
    payload = {
        "text": (f"[{comic['num']}] *{comic['safe_title']}*\n"
                 f"{comic['img']}\n"
                 f"(_alt text_) {comic['alt']}")
    }
    return jsonify(payload)

def get_comic_card(comic_number=""):
    """ Fetches comic info and returns a card-based response """
    r = requests.get("https://xkcd.com/{}/info.0.json".format(comic_number), headers=HEADERS)
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

def get_latest():
    """ Returns latest comic number """
    r = requests.get("https://xkcd.com/info.0.json", headers=HEADERS)
    return r.json()["num"]

def get_random_comic():
    """ Randomly picks a comic and returns a formatted response """
    latest = get_latest()
    random_comic_number = random.choice(range(1,int(latest)))
    return get_comic_text(random_comic_number)

def get_specific_comic(comic_number):
    """ Ensures a comic number exists first, then returns it in a formatted response """
    latest = get_latest()
    if int(comic_number) in range(1, int(latest) + 1):
        return get_comic_text(comic_number)
    else:
        return jsonify({"text": "Comic number '{}' not found".format(comic_number)})

def get_help_text():
    help_text = (f"Hi! I can help with all of your xkcd needs\n\n"
                 f"Actions:\n"
                 f"*Get the latest comic:* @{BOTNAME} latest\n"
                 f"*Get a random comic:* @{BOTNAME} random\n"
                 f"*Get a specific comic:* @{BOTNAME} <number>\n"
                 f"*Show this help message:* @{BOTNAME} help")
    return jsonify({"text": help_text})

def main(request):
    event_type = request.json["type"]
    if event_type == "MESSAGE":
        message = request.json["message"]["text"].split()
        # Remove @BOTNAME from message to handle both group chats and DMs
        if message[0] == "@{}".format(BOTNAME):
            message.pop(0)
        if not message or message[0].lower() == "latest":
            response = get_comic_text()
        elif message[0].lower() == "random":
            response = get_random_comic()
        elif re.match(r"[0-9]+", message[0]):
            response = get_specific_comic(message[0])
        else:
            response =  get_help_text()
    elif event_type == "ADDED_TO_SPACE":
        response = get_help_text()
    elif event_type == "REMOVED_FROM_SPACE":
        response = None

    return response
