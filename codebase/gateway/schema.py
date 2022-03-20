from pydantic import BaseModel
from typing import Optional

class CreateApi(BaseModel):

    """
    
    """
    path: str
    description: Optional[str]

class UpdateApi(BaseModel):

    """
    
    """
    #path: Optional[str]
    description:str

class DeleteApi(BaseModel):

    """
    
    """
    path: str

class CreateMock(BaseModel):

    """
    
    """
    path: str
    description: Optional[str]
    method: str
    reponse: str
    api_id: int

