import json
import logging
import azure.functions as func
from client import connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    players = req.params.get('players')
    if not players:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('players')

    container = connectToContainer('quiplashDB', 'prompts')

    if players == '-1':
        item_list = list(container.read_all_items(max_item_count=10))
        logging.info(item_list)
        return func.HttpResponse(json.dumps(item_list))
    elif players != '-1':
        prompts = []
        container = connectToContainer('quiplashDB', 'prompts')
        for p in players:
            if p.isnumeric():
                for items in container.query_items(query='SELECT p.id, p.text, p.username FROM prompts p WHERE p.username="{}"'.format(
                        p),
                        enable_cross_partition_query=True):
                    prompts.append(items)
        return func.HttpResponse(json.dumps(prompts))
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
