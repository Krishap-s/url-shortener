import typing

from fastapi import Depends
from fastapi import exceptions as faexceptions
from fastapi import routing

from authentication import is_admin
from infrastructure.db import get_db
from services.complaint import exceptions, schema, service
from services.users import schema as users_schemas

ComplaintRouter = routing.APIRouter(prefix="/complaint")
ComplaintService = service.Service(get_db())


@ComplaintRouter.post("/create_complaint", response_model=schema.Complaint)
async def create_complaint(
    inp: schema.CreateComplaintSchema,  # noqa: E501
):
    """Create new complaint"""
    try:
        return ComplaintService.create_complaint(inp)
    except exceptions.LinkNotFoundException:
        raise faexceptions.HTTPException(
            status_code=404, detail="link not found"
        )  # noqa: E501


@ComplaintRouter.get(
    "/get_complaints",
    response_model=typing.List[schema.Complaint],
)  # noqa: E501
async def get_complaints(
    link_key: str, user: users_schemas.User = Depends(is_admin)  # noqa: E501
):
    """Get complaints"""
    try:
        return ComplaintService.get_complaints_by_link(link_key)
    except exceptions.LinkNotFoundException:
        raise faexceptions.HTTPException(
            status_code=404, detail="link not found"
        )  # noqa: E501
