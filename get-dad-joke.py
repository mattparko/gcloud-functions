# Google Cloud Function / Python 3.7 runtime

# Currently only supports Google Hangouts Chat (due to event type handling)

import requests
import random
from flask import jsonify

def get_random_joke():
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    r = requests.get("https://icanhazdadjoke.com/", headers=headers)
    return r.json()["joke"]

def target_joke(name, requester):
    ids = {
        "john": "109387382268187184440",
        "parko": "117199954185662884890"
    }
    if name in ids:
        return "<users/{}> {}".format(ids[name], get_random_joke())
    else:
        return "I'm sorry, <{}>. I'm afraid I can't do that".format(requester)

def search_jokes(search_term):
    headers = {"Accept": "application/json", "Content-type": "application/json"}
    r = requests.get("https://icanhazdadjoke.com/search?term=" + search_term, headers=headers)
    jokes = r.json()["results"]
    if jokes:
        return random.choice(jokes)["joke"]
    else:
        return "No search results"

def get_help_text():
    return """
Hi! I can help with all of your Dad Joke needs

Actions:
*Get a random joke:* @DadBot random
*Search for a joke:* @DadBot search <query>
*Show this help message:* @DadBot help
"""

def main(request):
    event_type = request.json["type"]
    if event_type == "MESSAGE":
        message = request.json["message"]["text"].split()
        # Remove "@DadBot" from message to handle both group chats and DMs
        if message[0] == "@DadBot":
            message.pop(0)
        if message[0].lower() == "random":
            response = get_random_joke()
        elif message[0].lower() == "search":
            response = search_jokes(' '.join(message[1:]))
        # Easter egg for adding an "@" mention to the joke
        elif message[0].lower() == "troll":
            response = target_joke(message[1].lower(), request.json["message"]["sender"]["name"])
        else:
            response =  get_help_text()
    elif event_type == "ADDED_TO_SPACE":
        response = get_help_text()
    elif event_type == "REMOVED_FROM_SPACE":
        response = "What?! You don't like Dad Jokes!?"

    return jsonify({"text": response})
