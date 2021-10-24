import logging
import json
import azure.functions as func
from client import connectToContainer


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
        tmp = json.dumps(player[0])
        a = json.loads(tmp)
        if a["password"] == password:
            json_msg = {"result": True, "msg": "OK"}
            return func.HttpResponse(json.dumps(json_msg),
                                     status_code=200)
        else:
            json_msg = {"result": False,
                        "msg": "Username or password incorrect"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400)
    else:
        json_msg = {"result": False, "msg": "Username or password incorrect"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400)
