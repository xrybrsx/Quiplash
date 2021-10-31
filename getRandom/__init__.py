import json
import logging

import azure.functions as func
import random
from client import connectToContainer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    n = req.params.get("n")
    if not n:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            n = req_body.get('n')

    if n:
        container = connectToContainer("quiplashDB", "prompts")
        ids = []
        for item in container.query_items(
                query='SELECT p.id, p.text, p.username FROM prompts p',
                enable_cross_partition_query=True):
            logging.info(item)
            ids.append(item)
        random_ids = random.sample(ids, int(n))
        result = []
        for i in random_ids:
            result.append(i)
        return func.HttpResponse(json.dumps(result, separators=(',', ':')))
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
