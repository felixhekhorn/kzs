import binascii
import hashlib
import os
import pathlib

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class MyBase:
    id = Column(Integer, primary_key=True, autoincrement=True)

    def as_dict(self):
        d = {}
        for c in self.__table__.columns: # pylint: disable=no-member
            if c.name == "password":
                continue
            d[c.name] = getattr(self, c.name)
            if c.name == "ctime":
                d[c.name] = d[c.name].isoformat()
        return d


Base = declarative_base(cls=MyBase)


class User(Base):
    __tablename__ = "users"

    name = Column(String)
    password = Column(String)
    games = relationship("Game")

    # https://www.vitoshacademy.com/hashing-passwords-in-python/
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
        pwdhash = hashlib.pbkdf2_hmac("sha512", password.encode("utf-8"), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode("ascii")

    def verify_password(self, provided_password):
        """Verify a stored password against one provided by user"""
        stored_password = self.password
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac(
            "sha512", provided_password.encode("utf-8"), salt.encode("ascii"), 100000
        )
        pwdhash = binascii.hexlify(pwdhash).decode("ascii")
        return pwdhash == stored_password


class Game(Base):
    __tablename__ = "games"

    title = Column(String)
    slug = Column(String)
    state = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    ctime = Column(DateTime, server_default=func.now())
    players = relationship("Player")
    entries = relationship("Entry")

    def nextPlayer(self):
        """Compute the next player"""
        if len(self.entries) == 0:
            return self.players[0]
        le = self.entries[-1]
        lp = next(filter(lambda p: p.user_id == le.user_id, self.players))
        next_pos = (lp.position + 1) % len(self.players)
        np = next(filter(lambda p: p.position == next_pos, self.players))
        return np

    def serialize_json(self):
        """ "Returns JSON representation."""
        gg = self.as_dict()
        # add Players + Entries
        gg["players"] = [p.as_dict() for p in self.players]
        gg["entries"] = [e.as_dict() for e in self.entries]
        gg["next_player_user_id"] = self.nextPlayer().user_id
        return gg

    def collect_users(self, users):
        """Add all active Users to the map."""
        for p in self.players:
            if p.user.id not in users:
                users[p.user.id] = p.user


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
    ctime = Column(DateTime, server_default=func.now())
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
