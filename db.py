import pathlib

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
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
    user_id = Column(Integer, ForeignKey("users.id"))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    position = Column(Integer)
    body = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))


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
