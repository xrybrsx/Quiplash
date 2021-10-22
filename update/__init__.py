import logging
import json
import azure.functions as func
from client import connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        '----------------Python HTTP trigger function processed a request.----------------')
    # logging.info("The JSON received {}".format(req.params.get()))
    username = req.params.get('username')
    increment = int(req.params.get('add_to_games_played'))
    player = []

    if (not username):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    if username:
        container = connectToContainer('quiplashDB', 'players')

        for item in container.query_items(
                query='SELECT * FROM players p WHERE p.username="{}"'.format(
                    username),
                enable_cross_partition_query=True):
            logging.info(item)
            player.append(item)

    if (len(player) > 0) and (increment > 0):
        tmp = json.dumps(player[0])
        a = json.loads(tmp)
        a["games_played"] = a["games_played"] + increment
        query = container.upsert_item(a)
        okMessage = {"result": True,
                     "msg": "OK"}
        return func.HttpResponse(json.dumps(okMessage))
    elif ((len(player) <= 0)):
        noSuchUser = {"result": False,
                      "msg": "user does not exist"}
        return func.HttpResponse(json.dumps(noSuchUser))
    elif (increment < 0):
        negativeGames = {"result": False,
                         "msg": "Attempt to set negative score/games_played"}
        return func.HttpResponse(json.dumps(negativeGames))

    return func.HttpResponse("ok?")
