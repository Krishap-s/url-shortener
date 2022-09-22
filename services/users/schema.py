import pydantic


class CreateUserSchema(pydantic.BaseModel):
    username: str
    email: pydantic.EmailStr
    is_admin: bool
    password: str


class AuthenticateSchema(pydantic.BaseModel):
    username: str
    password: str


class User(pydantic.BaseModel):
    id: int
    username: str
    email: pydantic.EmailStr
    is_admin: bool
