from pydantic import AnyHttpUrl, BaseModel


class CreateLinkSchema(BaseModel):
    reference: AnyHttpUrl
    is_active: bool = True


class Link(BaseModel):

    key: str
    reference: AnyHttpUrl
    owner_id: int
    action: str
    is_active: bool

    class Config:
        orm_mode = True
