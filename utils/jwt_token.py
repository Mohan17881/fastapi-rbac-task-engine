from jose import jwt,JWTError
from datetime import datetime,UTC,timedelta

SECRETKEY = 'er8hwefiud920the92ndbv95'
ALGORITHM = 'HS256'
EXPIRE_MINUTES = 5

def create_jwt_token(data: dict):
    payload = data.copy()
    payload['exp'] = datetime.now(UTC) + timedelta(minutes=EXPIRE_MINUTES)
    try:
        token = jwt.encode(payload,SECRETKEY,algorithm=ALGORITHM)
        return token
    except JWTError as e:
        return f'error in creating token {e}'
    