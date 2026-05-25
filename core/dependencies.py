import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = "er8hwefiud920the92ndbv95"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        
        if email is None or user_id is None or role is None:
            raise exception
            
        return {"email": email, "id": user_id, "role": role}
        
    except jwt.PyJWTError:
        raise exception

def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted. Admin access required."
        )
    return current_user
