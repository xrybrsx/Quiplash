import logging
import json


import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    username = req.params.get('username')

    OK_message = {
        "result": "True",
        "msg": "OK",
        "username": username
    }
    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    if username:
        return func.HttpResponse(f"Hello {username}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )
        # return func.HttpResponse(
        #     "This HTTP triggered function executed successfully. Pass a username in the query string or in the request body for a personalized response.",
        #     status_code=200
        # )
