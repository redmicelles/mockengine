from fastapi import FastAPI, Request
from core.config import settings

app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION
        )

@app.get("/about")
async def about(request: Request):
    return {"message": "The about route exists in the backend", "response_source": "Main Backend"}

@app.post("/contact")
async def about(request: Request):
    return {"message": "The contact route exists in the backend", "response_source": "Main Backend"}