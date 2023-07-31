from fastapi import APIRouter
from .model.key import PublicKey, PrivateKey
from .depends import atlas
from collections.abc import AsyncIterator
from .util import async_list


router = APIRouter()
JWKAdapter = atlas(name='key', database='jwt-api')


@router.post('/')
async def hello_world():
    return {'message': 'hello world'}


@router.get('/public', response_model=list[PublicKey])
async def list_public_keys(collection: JWKAdapter):
    async def process() -> AsyncIterator[PublicKey]:
        for doc in collection.find():
            doc.pop('_id')
            private_key = PrivateKey(**doc)
            yield private_key.public_key
    return await async_list(process())
