from decimal import Clamped
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, null
from sqlalchemy.orm import relationship
from database.base_class import Base

class Mocks(Base):

    """
    This class creates the mock database table
    """
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, nullable=False)
    path = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer)
    response_body = Column(String, nullable=False)
    is_active = Column(Integer)
    date_created = Column(Date)

class BackendRoutes(Base):
    """
    DB of all registered Backend Routes
    """
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    path = Column(String, nullable=False, unique=True)
    method = Column(String, nullable=False)
    date_created = Column(Date)
