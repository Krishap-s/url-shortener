import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from settings import settings

app = fastapi.FastAPI(
    title="URL Shortener",
    description="A URL shortening service with more features",
    version="0.1.0",
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def healthcheck():
    return Response("OK")
