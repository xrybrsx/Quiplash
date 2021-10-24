import logging
import json
import azure.functions as func
from client import addPlayer, connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        '----------------Python HTTP trigger function processed a request.----------------')
    username = req.params.get('username')
    password = req.params.get('password')

    if (not username) or (not password):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            password = req_body.get('password')

    #logging.info(json.dumps(username), json.dumps(password))
    player = []
    if username:
        containerPlayers = connectToContainer('quiplashDB', 'players')
        for item in containerPlayers.query_items(
                query='SELECT * FROM players p WHERE p.username="{}"'.format(
                    username),
                enable_cross_partition_query=True):
            logging.info(item)
            player.append(item)

    if (len(player)) > 0:
        json_msg = {"result": False, "msg": "Username already exists"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=200)
    elif len(username) < 4:
        json_msg = {"result": False,
                    "msg": "Username less than 4 characters"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400
                                 )
    elif len(username) > 16:
        json_msg = {"result": False,
                    "msg": "Username more than 16 characters"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400
                                 )
    elif len(password) < 8:
        json_msg = {"result": False,
                    "msg": "Password less than 8 characters"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400
                                 )
    elif len(password) > 24:
        json_msg = {"result": False,
                    "msg": "Password more than 24 characters"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400
                                 )
    else:
        addPlayer(username, password)
        json_msg = {"result": True, "msg": "OK"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=200)
