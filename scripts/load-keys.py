from pathlib import Path
import json
from api.model.key import PrivateKey
import asyncio
from api.util import build_atlas_client
from api.config import Settings


def load_key(name: str) -> PrivateKey:
    source_path = Path(__file__).parent / 'local' / f'{name}'
    with (source_path / 'private-key.json').open('r') as f, (source_path / 'private-key.pem').open('r') as g:
        return PrivateKey(**json.load(f), pem=g.read().strip())


async def main():
    settings = Settings()
    mongo_client = build_atlas_client(atlas_host=settings.atlas_host)
    collection = mongo_client.get_database('jwt-api').get_collection('key')
    keys = [load_key(name='key1')]
    for key_data in keys:
        collection.insert_one(key_data.model_dump())

if __name__ == '__main__':
    asyncio.run(main())
