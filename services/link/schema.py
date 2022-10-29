from enum import Enum

from pydantic import AnyHttpUrl, BaseModel


class ActionEnum(str, Enum):
    REDIRECT = "REDIRECT"
    WARN = "WARN"
    BLOCK = "BLOCK"


class CreateLinkSchema(BaseModel):
    reference: AnyHttpUrl
    is_active: bool = True


class UpdateLinkSchema(BaseModel):
    key: str
    action: ActionEnum = ActionEnum.REDIRECT


class Link(BaseModel):

    key: str
    reference: AnyHttpUrl
    owner_id: int
    action: str
    is_active: bool

    class Config:
        orm_mode = True
