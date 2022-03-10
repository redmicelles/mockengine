from schemas.mocks import MocksCreate, BackendRoutesCreate
from database.models.mocks import Mocks, BackendRoutes
from sqlalchemy.orm import Session

def create_mock(mock: MocksCreate, db:Session):

    """
    Method for inserting rows into the Mock table
    """
    mock = Mocks(
        **mock.dict()
    )
    db.add(mock)
    db.commit()
    db.refresh(mock)

def create_backendroute(backendroute: BackendRoutesCreate, db:Session):

    """
    Method for inserting rows into the BackendRoutes table
    """
    backendroute = BackendRoutes(
        **backendroute.dict()
    )
    db.add(backendroute)
    db.commit()
    db.refresh(backendroute)