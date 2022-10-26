from pydantic import BaseModel


class CreateComplaintSchema(BaseModel):
    link_key: str
    body: str


class Complaint(BaseModel):

    id: int
    link_id: int
    body: str
    status: str

    class Config:
        orm_mode = True
