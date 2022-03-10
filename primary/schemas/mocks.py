from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MocksCreate(BaseModel):
    
    """
    Model for creating rows in Mock table
    """
    path: str
    project: str
    method: str
    status_code: int
    response_body: str
    is_active: int = 0
    date_created: str = datetime.now().date()

class MocksUpdate(BaseModel):

    """
    
    """
    is_active: int

class BackendRoutesCreate(BaseModel):
    
    """
    Model for creatng row in BackendRoutes table
    """
    project: str
    domain: str
    path: str
    method: str
    date_created: str = datetime.now().date()