import typing

from fastapi import Depends
from fastapi import exceptions as faexceptions
from fastapi import routing

from authentication import get_current_user, is_admin
from infrastructure.CassandraDB import get_cassandra_db
from infrastructure.db import get_db
from services.link import exceptions, schema, service
from services.users import schema as UserSchemas

LinkRouter = routing.APIRouter(prefix="/link")
LinkService = service.Service(get_db(), get_cassandra_db())


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


@LinkRouter.get("/get_links", response_model=typing.List[schema.Link])
def get_all_links(admin: UserSchemas.User = Depends(is_admin)):
    """Get all links"""
    return LinkService.get_all_links()


@LinkRouter.patch("/update_link_action/{key}", response_model=schema.Link)
def update_link_actio(
    key: str, admin: UserSchemas.User = Depends(is_admin)
):  # noqa:E501
    """Update link"""
    try:
        return LinkService.update_link(key)
    except exceptions.LinkNotFoundException:
        raise faexceptions.HTTPException(
            status_code=404, detail="link not found"
        )  # noqa:E501
