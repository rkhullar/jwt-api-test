from collections.abc import AsyncIterator
from fastapi import APIRouter, Body
from .depends import atlas
from .model.key import PrivateKey
from .util import async_list
from .schema.key import PublicKeysResponse, PublicKeyForClient
from .schema.oidc import DiscoveryMetadata, SignData
import jwt
import datetime as dt
import calendar

router = APIRouter()
JWKAdapter = atlas(name='key', database='jwt-api')
base_url = 'https://api-dev.example.nydev.me/jwt-server'


@router.get('/hello')
async def hello_world():
    return {'message': 'hello world'}


def to_epoch(timestamp: dt.datetime) -> int:
    # NOTE: don't use the following:
    # return int(timestamp.strftime('%s'))
    # NOTE: instead do this:
    return calendar.timegm(timestamp.timetuple())


@router.post('/test/payload', response_model=dict)
async def test_capture_payload(data: dict = Body(...)):
    return data


@router.post('/sign')
async def sign_data(collection: JWKAdapter, request: SignData):
    doc = collection.find_one()
    private_key = PrivateKey(**doc)

    return request

    # now = dt.datetime.utcnow()
    # exp = now + dt.timedelta(minutes=5)
    # jwt_metadata = dict(
    #     iss=base_url,
    #     aud='api://default',
    #     iat=to_epoch(now),
    #     exp=to_epoch(exp)
    # )
    # return jwt.encode(payload={**jwt_metadata, **data}, key=private_key.pem, algorithm='RS256', headers={'kid': private_key.kid})


@router.get('/public-keys', response_model=PublicKeysResponse)
async def list_public_keys(collection: JWKAdapter):
    async def process() -> AsyncIterator[PublicKeyForClient]:
        for doc in collection.find():
            doc.pop('_id')
            private_key = PrivateKey(**doc)
            public_key_data = private_key.public_key.model_dump()
            yield PublicKeyForClient(**public_key_data)
    return PublicKeysResponse(keys=await async_list(process()))


@router.get('/.well-known/openid-configuration', response_model=DiscoveryMetadata)
async def discovery_metadata():
    return DiscoveryMetadata(issuer=base_url, jwks_uri=f'{base_url}/public-keys')
