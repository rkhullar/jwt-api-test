from fastapi import APIRouter


router = APIRouter()


@router.post('/')
def hello_world():
    return {'message': 'hello world'}
