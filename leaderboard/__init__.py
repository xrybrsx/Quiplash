import logging
import json
import azure.cosmos
import azure.functions as func
from client import connectToClient, connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    top = req.params.get('top')

    if not top:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            top = req_body.get('top')

    if top:
        container = connectToContainer('quiplashDB', 'players')
        players = []

        for items in container.query_items(
                query='SELECT TOP {} p.username,p.games_played,p.total_score FROM players p ORDER BY p.username ASC'.format(
                    top),
                enable_cross_partition_query=True):
            players.append(items)

    return func.HttpResponse(json.dumps(players))
