from azure.cosmos import CosmosClient
import json


def connectToClient():
    ACCOUNT_URI = 'https://quiplash-db.documents.azure.com:443/'
    ACCOUNT_KEY = 'VhRMquRsPTGLdGcGhSsDkqmebqPRqxWtdh0HodaToPz3tEPxh85rveN9O1Br0yPST1b7Fnv9hhnYcAaly5jDgg=='
    client = CosmosClient(ACCOUNT_URI, credential=ACCOUNT_KEY)
    return client


def connectToContainer(database_name, container_name):
    client = connectToClient()
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    return container


def addPlayer(username, password):
    container = connectToContainer('quiplashDB', 'players')

    return container.upsert_item({
        "username": username,
        "password": password,
        "games_played": 0,
        "total_score": 0
    })


def authorize(username, password):
    player = get_user(username)
    if len(player) > 0:
        tmp = json.dumps(player[0])
        a = json.loads(tmp)
        return a["password"] == password
    else:
        return False


def get_user(username):
    player = []
    container = connectToContainer('quiplashDB', 'players')
    for item in container.query_items(
            query='SELECT * FROM players p WHERE p.username="{}"'.format(
                username),
            enable_cross_partition_query=True):
        player.append(item)
    return player


def update_user(username, add_games, add_score):
    player = get_user(username)
    if len(player) > 0:
        tmp = json.dumps(player[0])
        a = json.loads(tmp)
        a["games_played"] = a["games_played"] + add_games
        a["total_score"] = a["total_score"] + add_score
        container = connectToContainer('quiplashDB', 'players')
        container.upsert_item(a)
        return True
    else:
        return False


def userExists(username):
    player = get_user(username)
    if len(player) > 0:
        return True
    else:
        return False

# def updatePlayer(username, add_games):
#     container = connectToContainer('quiplashDB', 'players')

#     return container.upsert_item({
#         'username': username,
#         "games_played":
#     })
