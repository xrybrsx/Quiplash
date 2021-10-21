from azure.cosmos import CosmosClient


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


def addPlayer(username):
    container = connectToContainer('quiplashDB', 'players')

    return container.upsert_item({
        'username': username,
        "games_played": 0,
        "total_score": 0
    })

# def updatePlayer(username, add_games):
#     container = connectToContainer('quiplashDB', 'players')

#     return container.upsert_item({
#         'username': username,
#         "games_played":
#     })
