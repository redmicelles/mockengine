from sqlalchemy import Integer, String, Date
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class API(Base):

    """
    
    """
    __tablename__ = 'api'

    id: Column = Column(Integer, primary_key=True, index=True)
    path: Column = Column(String, nullable=False, unique=True)
    description: Column = Column(String, nullable=True)
    date_created: Column = Column(Date, default=datetime.now().date)
    mocks = relationship("Mock", back_populates="mock_owner")

class Mock(Base):

    """
    
    """
    __tablename__ = "mock"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    description = Column(String, nullable=True)
    method = Column(String, nullable=False)
    reponse = Column(String, nullable=False)
    api_id = Column(Integer, ForeignKey("api.id"))

    mock_owner = relationship("API", back_populates="mocks")