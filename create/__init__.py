import logging
import json
from typing import Text
import azure.functions as func
from client import connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')
    text = req.params.get('text')
    if (not username) or (not text):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            text = req_body.get('text')
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
                query='SELECT * FROM prompts p WHERE p.text="{}"'.format(
                    text),
                enable_cross_partition_query=True):
            logging.info(item)
            textExist.append(item)

    if (len(player) <= 0):
        NoSuchUser = {"result": False, "msg": "user does not exist"}
        return func.HttpResponse(json.dumps(NoSuchUser))
    elif (len(textExist)) > 0:
        return func.HttpResponse("there is such text")
    elif (len(str(text)) < 10):
        lessThan10 = {"result": False,
                      "msg": "prompt is less than 10 characters"}
        return func.HttpResponse(json.dumps(lessThan10))
    elif (len(str(text)) > 100):
        moreThan100 = {"result": False,
                       "msg": "prompt is more than 100 characters"}
        return func.HttpResponse(json.dumps(moreThan100))
    else:
        new_prompt = containerPrompts.upsert_item({
            'text': '{}'.format(text),
            'username': '{}'.format(username)
        })
        return func.HttpResponse(
            json.dumps(new_prompt),
            status_code=200
        )
