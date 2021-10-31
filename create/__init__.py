import logging
import json
from typing import Text
import azure.functions as func
from client import connectToContainer, authorize
import random


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')
    text = req.params.get('text')
    password = req.params.get('password')
    if (not username) or (not text) or (not password):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            text = req_body.get('text')
            password = req_body.get('password')
    player = []
    textExist = []

    if username:
        containerPlayers = connectToContainer('quiplashDB', 'players')
        containerPrompts = connectToContainer('quiplashDB', 'prompts')
        for item in containerPlayers.query_items(
                query='SELECT * FROM players p WHERE p.username="{}"'.format(
                    username),
                enable_cross_partition_query=True):
            logging.info(item)
            player.append(item)

        for item in containerPrompts.query_items(
                query='SELECT * FROM prompts p WHERE p.text="{}" AND p.username="{}"'.format(
                    text, username),
                enable_cross_partition_query=True):
            logging.info(item)
            textExist.append(item)

    if (len(player) <= 0):
        json_msg = {"result": False, "msg": "user does not exist"}
        return func.HttpResponse(json.dumps(json_msg), status_code=400)
    elif not authorize(username, password):
        json_msg = {"result": False, "msg": "bad username or password"}
        return func.HttpResponse(json.dumps(json_msg), status_code=400)
    elif (len(textExist)) > 0:
        json_msg = {"result": False,
                    "msg": "User already has a prompt with the same text"}
        return func.HttpResponse(json.dumps(json_msg), status_code=400)
    elif (len(str(text)) < 10):
        json_msg = {"result": False,
                    "msg": "prompt is less than 10 characters"}
        return func.HttpResponse(json.dumps(json_msg), status_code=400)
    elif (len(str(text)) > 100):
        json_msg = {"result": False,
                    "msg": "prompt is more than 100 characters"}
        return func.HttpResponse(json.dumps(json_msg), status_code=400)
    else:
        new_prompt = containerPrompts.upsert_item({
            'text': '{}'.format(text),
            'username': '{}'.format(username),
            'id': '{}'.format(random.randint(100, 1001))
        })
        json_msg = {"result": True, msg: "OK"}
        return func.HttpResponse(
            json.dumps(json_msg),
            status_code=200
        )
