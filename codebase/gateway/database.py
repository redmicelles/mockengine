from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:pass@pgdb:5432/postgres"

engine: create_engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
session_local: sessionmaker = sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine)

def get_db():
    db: session_local = session_local()
    try:
        yield db
    except:
        db.close()

    