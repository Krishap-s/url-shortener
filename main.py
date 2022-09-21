import fastapi

app = fastapi.FastAPI()

@app.get("/")
def healthcheck():
    return "OK"