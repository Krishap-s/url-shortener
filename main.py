import fastapi
from fastapi import security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from api.link import LinkRouter
from api.user import UserRouter
from settings import settings

app = fastapi.FastAPI(
    title="URL Shortener",
    description="A URL shortening service with more features",
    version="0.1.0",
    license_info={
        "name": "MIT",
    },
)

oauth2_scheme = security.OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healthcheck():
    return Response("OK")


app.include_router(UserRouter)
app.include_router(LinkRouter)
