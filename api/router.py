from collections.abc import AsyncIterator
from fastapi import APIRouter, Body
from .depends import atlas
from .model.key import PrivateKey
from .util import async_list
from .schema.key import PublicKeysResponse, PublicKeyForClient
import jwt

router = APIRouter()
JWKAdapter = atlas(name='key', database='jwt-api')


@router.get('/hello')
async def hello_world():
    return {'message': 'hello world'}


@router.post('/sign')
async def sign_data(collection: JWKAdapter, data: dict = Body(...)):
    doc = collection.find_one()
    private_key = PrivateKey(**doc)
    return jwt.encode(payload=data, key=private_key.pem, algorithm='RS256')


@router.get('/public-keys', response_model=PublicKeysResponse)
async def list_public_keys(collection: JWKAdapter):
    async def process() -> AsyncIterator[PublicKeyForClient]:
        for doc in collection.find():
            doc.pop('_id')
            private_key = PrivateKey(**doc)
            public_key_data = private_key.public_key.model_dump()
            yield PublicKeyForClient(**public_key_data)
    return PublicKeysResponse(keys=await async_list(process()))


'''
@router.get('/.well-known/oauth-authorization-server')
async def metadata():
    base_url = 'https://api-dev.example.nydev.me/jwt-server'
    return {
        'issuer': base_url,
        'jwks_uri': f'{base_url}/public-keys'
    }
'''


@router.get('/.well-known/openid-configuration')
async def metadata():
    base_url = 'https://api-dev.example.nydev.me/jwt-server'
    return {
        'issuer': base_url,
        'jwks_uri': f'{base_url}/public-keys'
    }
