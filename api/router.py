import calendar
import datetime as dt
from collections.abc import AsyncIterator

import jwt
from fastapi import APIRouter, Body

from .depends import ReadSettings, atlas
from .model.key import PrivateKey
from .schema.key import PublicKeyForClient, PublicKeysResponse
from .schema.oidc import DiscoveryMetadata, SignData, SignDataResponse
from .util import async_list

router = APIRouter()
JWKAdapter = atlas(name='key', database='jwt-api')


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


@router.post('/sign', response_model=SignDataResponse)
async def sign_data(collection: JWKAdapter, settings: ReadSettings, request: SignData):
    doc = collection.find_one()
    private_key = PrivateKey(**doc)
    now = dt.datetime.utcnow()
    exp = now + dt.timedelta(seconds=request.metadata.duration)
    jwt_metadata = dict(
        iss=settings.issuer_url,
        aud=request.metadata.audience,
        iat=to_epoch(now),
        exp=to_epoch(exp)
    )
    return SignDataResponse(
        access_token=jwt.encode(payload={**jwt_metadata, **request.data}, key=private_key.pem, algorithm='RS256', headers={'kid': private_key.kid})
    )


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
async def discovery_metadata(settings: ReadSettings):
    return DiscoveryMetadata(issuer=settings.issuer_url, jwks_uri=f'{settings.issuer_url}/public-keys')
