import logging

import azure.functions as func

from client import authorize, connectToContainer
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.params.get('id')
    text = req.params.get('text')
    username = req.params.get('username')
    password = req.params.get('password')

    if (not username) or (not password) or (not id) or (not text):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')
            password = req_body.get('password')
            text = req_body.get('text')
            id = req_body.get('id')

    ids = []
    if id:
        containerPrompts = connectToContainer('quiplashDB', 'prompts')
        for item in containerPrompts.query_items(
                query='SELECT * FROM prompts p WHERE p.id="{}"'.format(
                    id),
                enable_cross_partition_query=True):
            logging.info(item)
            ids.append(item)

    if not authorize(username, password):
        json_msg = {"result": False, "msg": "bad username or password"}
        return func.HttpResponse(json.dumps(json_msg))
    elif (len(text) < 10):
        json_msg = {"result": False,
                    "msg": "prompt is less than 10 characters"}
        return func.HttpResponse(json.dumps(json_msg))
    elif (len(text) > 100):
        json_msg = {"result": False,
                    "msg": "prompt is more than 100 characters"}
        return func.HttpResponse(json.dumps(json_msg))
    elif(len(ids) <= 0):
        json_msg = {"result": False, "msg": "prompt id does not exist"}
        return func.HttpResponse(json.dumps(json_msg))
    elif json.loads(json.dumps(ids[0]))["text"] == text:
        json_msg = {"result": False,
                    "msg":  "user already has a prompt with the same text"}
        return func.HttpResponse(json.dumps(json_msg))
    else:
        tmp = json.dumps(ids[0])
        a = json.loads(tmp)
        a["text"] = text
        container = connectToContainer('quiplashDB', 'prompts')
        container.upsert_item(a)
        json_msg = {"result": True, "msg": "OK"}
        return func.HttpResponse(json.dumps(json_msg),
                                 status_code=200
                                 )
