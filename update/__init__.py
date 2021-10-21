import logging
import json
import azure.functions as func
from client import addPlayer


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(
        '----------------Python HTTP trigger function processed a request.----------------')
    logging.info("The JSON received {}".format(req.get_json()))
    username = req.params.get('username')

    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    if username:
        addPlayer(username)
        return func.HttpResponse(f"Hello, {username}. Your profile was created.")
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
    else:
        return func.HttpResponse(
            " Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )
