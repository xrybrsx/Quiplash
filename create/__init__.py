import logging
import json
import uuid
from azure.cosmos import CosmosClient
import azure.functions as func
import os

url = os.environ['https://quiplash-db.documents.azure.com:443/']
key = os.environ['VhRMquRsPTGLdGcGhSsDkqmebqPRqxWtdh0HodaToPz3tEPxh85rveN9O1Br0yPST1b7Fnv9hhnYcAaly5jDgg==']
client = CosmosClient(url, credential=key)


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')

    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    if username:
        newdocs = func.DocumentList()
        newproduct_dict = {
            "id": str(uuid.uuid4()),
            "name": username
        }
        newdocs.append(func.Document.from_dict(newproduct_dict))
        doc.set(newdocs)
        return func.HttpResponse(f"Hello, {username}. Your profile was created.")

    else:
        return func.HttpResponse(
            " Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
