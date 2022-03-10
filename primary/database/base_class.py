from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:

    """
    This is the base class for every other
    SQLAlchemy class
    """
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls)->str:

        """
        This class method generates db table name 
        from class name
        """
        return cls.__name__.lower()