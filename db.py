import pathlib

from sqlalchemy import Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class MyBase:
    id = Column(Integer, primary_key=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=MyBase)


class User(Base):
    __tablename__ = "users"

    name = Column(String)
    games = relationship("Game")


class Game(Base):
    __tablename__ = "games"

    title = Column(String)
    slug = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    players = relationship("Player")
    entries = relationship("Entry")

    def nextPlayer(self):
        if len(self.entries) == 0:
            return self.players[0]
        le = self.entries[-1]
        lp = next(filter(lambda p: p.user_id == le.user_id, self.players))
        next_pos = (lp.position + 1) % len(self.players)
        print(lp.user_id, lp.position)
        print(next_pos)
        np = next(filter(lambda p: p.position == next_pos, self.players))
        print(np.user_id, np.position)
        return np


class Player(Base):
    __tablename__ = "players"

    position = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    user = relationship("User")


class Entry(Base):
    __tablename__ = "entries"

    body = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    user = relationship("User")


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
