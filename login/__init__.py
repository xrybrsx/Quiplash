import logging
import json
import azure.functions as func
from client import authorize


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

    if authorize(username, password):
        json_msg = {"result": True, "msg": "OK"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=200)
    else:
        json_msg = {"result": False,
                    "msg": "Username or password incorrect"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=400)
