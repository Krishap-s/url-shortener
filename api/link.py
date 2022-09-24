from fastapi import Depends
from fastapi import exceptions as faexceptions
from fastapi import routing

from authentication import get_current_user
from infrastructure.db import get_db
from services.link import exceptions, schema, service
from services.users import schema as UserSchemas

LinkRouter = routing.APIRouter(prefix="/link")
LinkService = service.Service(get_db())


@LinkRouter.post("/", response_model=schema.Link)
def create_link(
    inp: schema.CreateLinkSchema,
    user: UserSchemas.User = Depends(get_current_user),  # noqa:E501
):
    """Create new shortened url"""
    return LinkService.create_link(inp, user.id)


@LinkRouter.get("/{key}")
def get_link(key):
    """Get reference url"""
    try:
        res = LinkService.get_link_by_key(key)
        return {"link": res.reference}
    except exceptions.LinkNotFoundException:
        raise faexceptions.HTTPException(
            status_code=404, detail="link not found"
        )  # noqa:E501
