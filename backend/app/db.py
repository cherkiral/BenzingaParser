from pymongo import MongoClient
from os import getenv


async def get_database():
    CONNECTION_STRING = getenv("MONGODB_URL")

    client = MongoClient(CONNECTION_STRING)

    return client['news']
