from fastapi import FastAPI, Depends, status, Request
from fastapi.exceptions import HTTPException
from schema import CreateApi, UpdateApi, DeleteApi, CreateMock
from sqlalchemy.orm import Session
from database import get_db
from models import API, Mock
import os

app = FastAPI()

@app.get("/")
def index()->dict:

    return {"details": "You are doing well"}

#API Manager
@app.post("/register_api", tags=["Manage APIs"])
def create_api(details: CreateApi, db: Session=Depends(get_db))->dict:

    to_create = API(
        path=details.path,
        description=details.description
    )
    query = db.query(API).filter(API.path==details.path).first()
    if query:
        return {
        "details":"record already exist",
        "status_code": status.HTTP_404_NOT_FOUND
        }
    db.add(to_create)
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "created_record_id": to_create.id
    }

@app.get("/retrieve_api/{path}", tags=["Manage APIs"])
def retreive_api_by_path(path: str, db: Session=Depends(get_db))->dict:

    query = db.query(API).filter(API.path==path).one_or_none()

    if not query:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "details": "The requested record does not exist"
        }

    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.get("/retrieve_api", tags=["Manage APIs"])
def retreive_apis(db: Session=Depends(get_db))->dict:

    query = db.query(API).all()
    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.put("/edit_api/{path}", tags=["Manage APIs"])
def edit_api(path: str, details: UpdateApi, db: Session=Depends(get_db))->dict:

    query = db.query(API).filter(API.path==path).one_or_none()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The requested record does not exist")

    for key, val in vars(details).items():
        setattr(query, key, val) if val else None

    db.add(query)
    db.commit()
    db.refresh(query)

    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.delete("/delete_api/{path}", tags=["Manage APIs"])
def delete_api(path: str, db: Session=Depends(get_db))->dict:

    query = db.query(API).filter(API.path==path).one_or_none()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The requested record does not exist")
    deleted_record = query
    db.delete(query)
    db.commit()
    return {
            "status_code": status.HTTP_200_OK,
            "details": deleted_record
        }

#Mock Manager
@app.post("/register_mock", tags=["Manage Mocks"])
def create_mock(details: CreateMock, db: Session=Depends(get_db))->dict:

    to_create = Mock(
        path = details.path,
        description = details.description,
        method = details.method,
        reponse = details.reponse,
        api_id = details.api_id
    )
    api_query = db.query(API).filter(API.id==details.api_id).one_or_none()

    if not api_query:
        return {
        "details":"the reference API does not exist in the database",
        "status_code": status.HTTP_404_NOT_FOUND
        }
    mock_query = db.query(Mock).filter(Mock.api_id==details.api_id).\
    filter(Mock.path==details.path).one_or_none()
    
    if mock_query:
         return {
        "details":"this mock already exist",
        "status_code": status.HTTP_404_NOT_FOUND
        }
    db.add(to_create)
    db.commit()
    return {
        "status_code": status.HTTP_201_CREATED,
        "created_record_id": to_create.id
    }

@app.get("/retrieve_mock/{api_id}/{path}", tags=["Manage Mocks"])
def retreive_mock_by_path(api_id: str, path: str, db: Session=Depends(get_db))->dict:

    query = db.query(Mock).filter(Mock.api_id==api_id).filter(Mock.path==path).one_or_none()

    if not query:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "details": "The requested records do not exist"
        }

    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.get("/retrieve_mocks/{api_id}", tags=["Manage Mocks"])
def retreive_mocks_by_api_id(api_id: str, db: Session=Depends(get_db))->dict:

    query = db.query(Mock).join(API).filter(Mock.api_id==api_id).all()

    if not query:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "details": "The requested records do not exist"
        }

    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.get("/retrieve_mocks", tags=["Manage Mocks"])
def retreive_mocks(db: Session=Depends(get_db))->dict:

    query = db.query(Mock).join(API).all()

    if not query:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "details": "The requested records do not exist"
        }

    return {
        "status_code": status.HTTP_200_OK,
        "details": query
    }

@app.put("/edit_mock/{api_id}/{path}", tags=["Manage Mocks"])
def edit_mock(api_id: str, path: str, details: CreateMock, db: Session=Depends(get_db))->dict:
    
    api_query = db.query(API).filter(API.id==details.api_id)
    
    if not api_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The referenced API does not exist")
                            
    mock_query = db.query(Mock).filter(Mock.api_id==api_id).filter(Mock.path==path).one_or_none()

    if not mock_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The requested record does not exist {mock_query}")

    for key, val in vars(details).items():
        setattr(mock_query, key, val) if val else None

    db.add(mock_query)
    db.commit()
    db.refresh(mock_query)

    return {
        "status_code": status.HTTP_200_OK,
        "details": mock_query
    }

@app.delete("/delete_mock/{api_id}/{path}", tags=["Manage Mocks"])
def delete_mock(api_id: str, path: str, db: Session=Depends(get_db))->dict:

    api_query = db.query(API).filter(API.id==api_id)
    
    if not api_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The referenced API does not exist")

    query = db.query(Mock).filter(Mock.api_id==api_id).filter(Mock.path==path).one_or_none()

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The requested record does not exist")
    deleted_record = query
    db.delete(query)
    db.commit()
    return {
            "status_code": status.HTTP_200_OK,
            "details": deleted_record
        }

#Annonymous Routes
@app.get("/{full_path:path}", tags=["Anonymous Paths"])
def anonymous_routes(request: Request, full_path: str, db: Session=Depends(get_db)):

    referer = str(request.headers.get("referer"))
    path_ = os.path.split(referer)[1]
    method = request.method
    print(type(path_))
    query =  db.query(Mock).filter(Mock.path==path_).one_or_none()
    return {"message": query}

@app.post("/{full_path:path}", tags=["Anonymous Paths"])
def anonymous_routes(request: Request, full_path: str):

    return {"message": "all post routes accepted here"}

@app.put("/{full_path:path}", tags=["Anonymous Paths"])
def anonymous_routes(request: Request, full_path: str):

    return {"message": "all put routes accepted here"}

@app.patch("/{full_path:path}", tags=["Anonymous Paths"])
def anonymous_routes(request: Request, full_path: str):
    
    return {"message": "all patch routes accepted here"}

@app.delete("/{full_path:path}", tags=["Anonymous Paths"])
def anonymous_routes(request: Request, full_path: str):

    return {"message": "all delete routes accepted here"}