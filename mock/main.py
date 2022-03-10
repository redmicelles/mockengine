from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from starlette.types import ASGIApp, Scope, Receive, Send
from database.session import engine
from database.session import get_db
from sqlalchemy.orm import Session
from database.models.mocks import Mocks


def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION
        )
    return app

app = start_application()

@app.get("/{full_path:path}")
async def anonymous_routes(request: Request, full_path: str, db:Session=Depends(get_db)):
    #grab anonymous request path
    req_path = request.scope.get("path")[1:]
    req = {}
    try:
        req = await request.json()
    except:
        pass
    project = req.get("project")
    print(req)
    req_path = request.scope.get("path") #path detected from request
    data = db.query(Mocks).filter(Mocks.project==project).all() #check if same path exist in db
    if data:
        if data.is_active:
            return {"response": data.response_body, "response_source": "Mock Engine"}
    return {"details": "Endpoint does not exist in mock engine"}

@app.post("/{full_path:path}")
async def anonymous_routes(request: Request, full_path: str):

    params = await request.json()
    print(params)
    return {"message": "all post routes accepted here"}

@app.put("/{full_path:path}")
def anonymous_routes(request: Request, full_path: str):

    return {"message": "all put routes accepted here"}

@app.patch("/{full_path:path}")
def anonymous_routes(request: Request, full_path: str):
    
    return {"message": "all patch routes accepted here"}