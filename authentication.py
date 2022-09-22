import fastapi
import jwt
from fastapi import exceptions, security, status

from infrastructure.db import get_db
from services.users import service
from settings import settings

UserService = service.Service(get_db())

oauth2_scheme = security.HTTPBearer()


async def get_current_user(
    credentials: security.HTTPAuthorizationCredentials = fastapi.Depends(
        oauth2_scheme
    ),  # noqa: E501
):
    credentials_exception = exceptions.HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token.encode(), settings.secret_key, algorithms=["HS256"]
        )  # noqa: E501
        print(payload)
        id: int = payload.get("sub")
        user = UserService.get_user_by_id(id)
        if int is None:
            raise credentials_exception
        return user
    except Exception as e:
        print(e)
        raise credentials_exception
