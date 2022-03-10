"""
1. Requests headers should be used to reconstruct urls, then the url compared with those existing
in the database. If the request body does not specify the destination, the backend db table is first checked
and if a match is found, the request is send to the corresponding url, else the mock tables is checked for a
match, if found the response stored for the url is returned. Otherwise a not found error is returned.
2. Any request with a destination is routed directly to it destination without going through process 1.
3. All response will include response origin in their headers
"""

from fastapi import FastAPI, Request, Depends
from core.config import settings
from database.session import engine
from database.base import Base
from schemas.mocks import MocksCreate, MocksUpdate, BackendRoutesCreate
from database.repo.mocks import create_mock, create_backendroute
from database.session import get_db
from sqlalchemy.orm import Session
from database.models.mocks import Mocks, BackendRoutes
import requests

def create_tables():

    """
    This function create db tables
    """
    Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        version=settings.PROJECT_VERSION
        )
    create_tables()
    return app

app = start_application()

@app.post("/create_mock", tags=["Mocks"])
def createMock(request: Request, mock: MocksCreate, db:Session=Depends(get_db)):

    """
    This route handles creation of new mocks using
    the parameters
    path: str
    method: str
    """
    mock = create_mock(mock, db)
    return mock

@app.get("/mocks", tags=["Mocks"])
def list_mocks(request: Request, db:Session=Depends(get_db), skip: int = 0, limit: int = 100):

    """
    This route function returns all mocks in the database
    """
    result = db.query(Mocks).offset(skip).limit(limit).all()
    return {"mocks": result}

@app.put("/activate", tags=["Mocks"])
def activate_mock(request: Request, project:str, path: str, mock: MocksUpdate, db:Session=Depends(get_db)):

    """
    This route function updates the mock's status to active
    so as to enable it respond to requests
    """
    db_path = db.query(Mocks).filter(Mocks.project==project).filter(Mocks.path==path) #check if same path exist in db

    if not db_path.first():
        return {"details": "Not found"}

    mock.__dict__.update(is_active=1)
    db_path.update(mock.__dict__)
    db.commit()
    return {"details": "Mock activation was successful"}

@app.put("/deactivate", tags=["Mocks"])
def deactivate_mock(request: Request, project:str, path: str, mock: MocksCreate, db:Session=Depends(get_db)):

    """
    This route function updates the mock's status to inactive
    so as to prevent it from responding to requests
    """
    db_path = db.query(Mocks).filter(Mocks.project==project).filter(Mocks.path==path) #check if same path exist in db

    if not db_path:
        return {"details": "Not found"}

    mock.__dict__.update(is_active=0)
    db_path.update(mock.__dict__)
    db.commit()
    return {"details": "Mock deactivation was successful"}

@app.delete("/delete_mock", tags=["Mocks"])
def delete_mock(request: Request, project:str, path:str, db:Session=Depends(get_db)):

    """
    This route funtion deletes a mock using it path name
    """
    mock_to_delete = db.query(Mocks).filter(Mocks.project==project).filter(Mocks.path==path).first()
    mock = db.query(Mocks).get(mock_to_delete.id)
    db.delete(mock)
    db.commit()
    return {"deleted mock": mock_to_delete}


@app.post("/create_backendurl", tags=["Backend URLs"])
def createBackendurl(request: Request, backend_route: BackendRoutesCreate, db:Session=Depends(get_db)):

    """
    This route handles creation of new backend url using
    the parameters provided
    """
    backend_route = create_backendroute(backend_route, db)
    return backend_route

@app.get("/backend_urls", tags=["Backend URLs"])
def list_backend_urls(request: Request, db:Session=Depends(get_db), skip: int = 0, limit: int = 100):

    """
    This route function returns all backend urls in the database
    """
    result = db.query(BackendRoutes).offset(skip).limit(limit).all()
    return {"mocks": result}

@app.put("/edit_backendurl", tags=["Backend URLs"])
async def edit_backendurl(request: Request, path: str, project:str, backend_route: BackendRoutesCreate, db:Session=Depends(get_db)):

    """
    This route function updates the backend_url details
    """
    req = await request.json()
    backend_route_to_edit = db.query(BackendRoutes).filter(BackendRoutes.project==project).filter(BackendRoutes.path==path)#check if same path exist in db
    
    if not backend_route_to_edit.first():
        return {"details": "Not found"}

    for itm in req:
        backend_route.__dict__[itm] = req.get(itm)

    backend_route_to_edit.update(backend_route.__dict__)
    db.commit()
    return {"details": "Mock deactivation was successful"}

@app.delete("/delete_backendurl", tags=["Backend URLs"])
def delete_mock(request: Request, path:str, project:str, db:Session=Depends(get_db)):

    """
    This route funtion deletes a backendurl using its name
    """
    backendurl_to_delete = db.query(BackendRoutes).filter(BackendRoutes.project==project).filter(BackendRoutes.path==path).first()
    backend_url = db.query(BackendRoutes).get(backendurl_to_delete.id)
    db.delete(backend_url)
    db.commit()
    return {"deleted mock": backend_url}

@app.get("/{full_path:path}", include_in_schema=False)
async def call_middleware(request: Request, full_path: str, db:Session=Depends(get_db)):
    #request body should include project, and may include destination
    req: dict = {}
    #grab anonymous request path
    req_path = request.scope.get("path")[1:]
    try:
        req = await request.json()
    except:
        pass
    
    project, destination = req.get("project"), req.get("destination")

    #verify if request path is registered to the referenced project in the db
    backend_data = db.query(BackendRoutes).filter(BackendRoutes.project==project).filter(BackendRoutes.path==req_path).first()
    mock_data = db.query(Mocks).filter(Mocks.project==project).filter(Mocks.path==req_path).first()

    if destination:
        if destination.lower() == "backend" and not backend_data:
            return {"detail": f"The requested endpoint does not exist on the {project} backend"}
        elif destination.lower() == "mock" and not mock_data:
            return {"detail": f"The requested endpoint does not exist on the {project} mock"}
        elif destination.lower() == "backend" and backend_data:
            response = requests.get(f"http://{backend_data.domain}/{req_path}")
            return response.json()
        #pending bug fix for mock_data
        elif destination.lower() == "mock":
            response = requests.get(f"{settings.MOCK}/about")
            return response.json()
        return {"details": "this endpoint does not exist as a backend url or mock"}
    else:
        if backend_data:
            response = requests.get(f"http://{backend_data.domain}/{req_path}")
            return response.json()
        elif mock_data:
            response = requests.get(f"{settings.MOCK}/about")
            return response.json()
        return {"details": "this endpoint does not exist as a backend url or mock"}


@app.post("/{full_path:path}", include_in_schema=False)
async def call_middleware(request: Request, full_path: str):
    pass

@app.put("/{full_path:path}", include_in_schema=False)
async def call_middleware(request: Request, full_path: str):
    pass

@app.patch("/{full_path:path}", include_in_schema=False)
async def call_middleware(request: Request, full_path: str):
   pass

@app.delete("/{full_path:path}", include_in_schema=False)
async def call_middleware(request: Request, full_path: str):
    pass
# https://fastapi.tiangolo.com/advanced/path-operation-advanced-configuration/
