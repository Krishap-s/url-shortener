import fastapi
from fastapi import exceptions, routing, status
from jose import jwt
from sqlalchemy import exc

from authentication import get_current_user
from infrastructure.db import get_db
from services.users import exceptions as ServiceExceptions
from services.users import schema, service
from settings import settings

UserRouter = routing.APIRouter(prefix="/user")
UserService = service.Service(get_db())


@UserRouter.post("/", response_model=schema.User)
def register_user(inp: schema.CreateUserSchema):
    """Register User Route"""
    try:
        user = UserService.create_user(inp)
        return user
    except exc.IntegrityError:
        raise exceptions.HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with similar username or email already exists",
        )


@UserRouter.post("/login")
def login(inp: schema.AuthenticateSchema):
    """Login User Route"""
    try:
        user = UserService.authenticate(inp)
    except ServiceExceptions.InvalidCredentials:
        raise exceptions.HTTPException(
            status_code=401, detail="Invalid Username or password"
        )
    to_encode = {"sub": user.id}
    access_token = jwt.encode(
        to_encode, settings.secret_key, algorithm="HS256"
    )  # noqa: E501
    return {"access_token": access_token, "token_type": "bearer"}


@UserRouter.get("/me", response_model=schema.User)
def get_logged_in_user(user: str = fastapi.Depends(get_current_user)):
    """Get current logged in user"""
    return user
