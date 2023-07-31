from typing import Annotated

from fastapi import Depends, Request
from pymongo import MongoClient
from pymongo.database import Collection


def atlas(name: str, database: str = 'default'):
    def dependency(request: Request) -> Collection:
        mongo_client: MongoClient = request.app.extra['atlas']
        return mongo_client.get_database(database).get_collection(name)
    return Annotated[Collection, Depends(dependency)]
