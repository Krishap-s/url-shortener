from pydantic import AnyHttpUrl, BaseModel


class CreateLinkSchema(BaseModel):
    reference: AnyHttpUrl
    owner_id: int
    action: str

    class Config:
        orm_mode = True


class Link(BaseModel):

    id: int
    key: str
    reference: AnyHttpUrl
    owner_id: int
    action: str
    is_active: bool

    class Config:
        orm_mode = True
