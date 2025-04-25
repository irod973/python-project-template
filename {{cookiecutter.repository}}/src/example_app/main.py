# Ensure to install before running
from fastapi import FastAPI

app = FastAPI()

@app.get("/")  # type: ignore
def hello_world() -> dict[str, str]:
    return {"Hello": "World"}
