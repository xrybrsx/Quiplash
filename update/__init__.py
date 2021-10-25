import logging
import json
import azure.functions as func
from client import authorize, connectToContainer, update


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        '----------------Python HTTP trigger function processed a request.----------------')
    # logging.info("The JSON received {}".format(req.params.get()))
    username = req.params.get('username')
    add_games = req.params.get('add_to_games_played')
    add_score = req.params.get('add_to_score')
    password = req.params.get('password')

    player = []

    if (not username):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
    if not add_games:
        add_games = 0
    else:
        add_games = int(add_games)
    if not add_score:
        add_score = 0
    else:
        add_score = int(add_score)

    if username:
        container = connectToContainer('quiplashDB', 'players')

        for item in container.query_items(
                query='SELECT * FROM players p WHERE p.username="{}"'.format(
                    username),
                enable_cross_partition_query=True):
            logging.info(item)
            player.append(item)

    if ((len(player) <= 0)):
        json_msg = {"result": False,
                    "msg": "user does not exist"}
        return func.HttpResponse(json.dumps(json_msg))
    elif (int(add_games) < 0) or (int(add_score) < 0):
        json_msg = {"result": False,
                    "msg": "Attempt to set negative score/games_played"}
        return func.HttpResponse(json.dumps(json_msg))
    elif not authorize(username, password):
        json_msg = {"result": False, "msg": "wrong password"}
        return func.HttpResponse(json.dumps(json_msg))
    else:
        update(username, add_score, add_games)
        json_msg = {"result": True,
                    "msg": "OK"}

        return func.HttpResponse(json.dumps(json_msg))
