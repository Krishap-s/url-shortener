from pydantic import AnyHttpUrl, BaseModel


class CreateLinkSchema(BaseModel):
    reference: AnyHttpUrl
    action: str


class Link(BaseModel):

    id: int
    key: str
    reference: AnyHttpUrl
    owner_id: int
    action: str
    is_active: bool

    class Config:
        orm_mode = True
