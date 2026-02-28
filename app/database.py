from contextlib import contextmanager
<<<<<<< HEAD
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from . import models

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}

engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_all():
    SQLModel.metadata.drop_all(bind=engine)


=======
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends
from . import models


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_all():
    SQLModel.metadata.drop_all(bind=engine)

>>>>>>> 9ce0339a578e6c3b77727b5d689696ea4529cf92
@contextmanager
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]