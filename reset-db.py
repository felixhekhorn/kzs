import datetime
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, Entry, Game, Player, User, engine

# open connection

# open connection
uri = os.getenv("DATABASE_URL")
if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    eng = create_engine(uri, connect_args={"sslmode": "require"})
else:
    eng = engine("database.db")

Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)
Session = sessionmaker(bind=eng)
ses = Session()

# add initial data
# 1. users
uA = User(name="A", password="A")
uB = User(name="B", password="B")
uC = User(name="C", password="C")
uD = User(name="D", password="D")
ses.add_all([uA, uB, uC, uD])
ses.commit()
# 2. games
gA1 = Game(
    title="A1 running",
    user_id=uA.id,
    slug="gA1",
    state="running",
    ctime=datetime.datetime.now() - datetime.timedelta(minutes=65),
)
gB1 = Game(
    title="B1 init",
    user_id=uB.id,
    slug="gB1",
    state="init",
    ctime=datetime.datetime.now() - datetime.timedelta(hours=25),
)
gC1 = Game(
    title="C1 finished",
    user_id=uC.id,
    slug="gC1",
    state="finished",
    ctime=datetime.datetime.now() - datetime.timedelta(days=367),
)
gA2 = Game(title="A2 init", user_id=uA.id, slug="gA2", state="init")
ses.add_all([gA1, gB1, gC1, gA2])
ses.commit()
# 3. players + entries
ses.add_all(
    [
        # gA1
        Player(position=0, user_id=uA.id, game_id=gA1.id),
        Player(position=1, user_id=uB.id, game_id=gA1.id),
        Player(position=2, user_id=uC.id, game_id=gA1.id),
        # gB1
        Player(position=0, user_id=uB.id, game_id=gB1.id),
        Player(position=1, user_id=uA.id, game_id=gB1.id),
        Player(position=2, user_id=uC.id, game_id=gB1.id),
        # gC1
        Player(position=0, user_id=uC.id, game_id=gC1.id),
        Player(position=1, user_id=uA.id, game_id=gC1.id),
        Player(position=2, user_id=uB.id, game_id=gC1.id),
        # gA2
        Player(position=0, user_id=uA.id, game_id=gA2.id),
        Player(position=1, user_id=uB.id, game_id=gA2.id),
    ]
)
ses.add_all(
    [
        # gA1
        Entry(body="bla", user_id=uA.id, game_id=gA1.id),
        Entry(body="blabla", user_id=uB.id, game_id=gA1.id),
        # gC1
        Entry(body="this is", user_id=uC.id, game_id=gC1.id),
        Entry(body="the end", user_id=uA.id, game_id=gC1.id),
    ]
)
ses.commit()
