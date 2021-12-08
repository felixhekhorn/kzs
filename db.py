import pathlib

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    games = relationship("Game")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



# thanks banana!
def engine(
    path="",
    dialect="sqlite",
    driver=None,
    username=None,
    password=None,
    host=None,
    port=None,
):
    # Create an engine that stores data in the local directory
    infrastructure = dialect
    if driver is not None:
        infrastructure += f"+{driver}"
    login = ""
    if username is not None and password is not None:
        login = f"{username}:{password}@"
    address = ""
    if host is not None:
        address += f"{host}"
    if port is not None:
        address += f":{port}"
    if path:
        path = "/" + str(pathlib.Path(path).absolute())

    return create_engine(f"{infrastructure}://{login}{address}{path}")


# thanks banana!
def create_db(base_cls, engine):
    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    base_cls.metadata.create_all(engine)
