import datetime

from sqlalchemy.orm import sessionmaker

from db import Base, Entry, Game, Player, User, engine

# open connection

eng = engine("database.db")
Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)
Session = sessionmaker(bind=eng)
ses = Session()

# add initial data
ses.add_all(
    [
        User(id=1, name="A", password="A"),
        User(id=2, name="B", password="B"),
        User(id=3, name="C", password="C"),
        User(id=4, name="D", password="D"),
    ]
)
ses.add_all(
    [
        Game(
            id=1,
            title="A1 running",
            user_id=1,
            slug="gA1",
            state="running",
            ctime=datetime.datetime.now() - datetime.timedelta(minutes=65),
        ),
        Game(
            id=2,
            title="B1 init",
            user_id=2,
            slug="gB1",
            state="init",
            ctime=datetime.datetime.now() - datetime.timedelta(hours=25),
        ),
        Game(
            id=3,
            title="C1 finished",
            user_id=3,
            slug="gC1",
            state="finished",
            ctime=datetime.datetime.now() - datetime.timedelta(days=367),
        ),
        Game(id=4, title="A2 init", user_id=1, slug="gA2", state="init"),
    ]
)
ses.add_all(
    [
        # gA1
        Player(id=1, position=0, user_id=1, game_id=1),
        Player(id=2, position=1, user_id=2, game_id=1),
        Player(id=3, position=2, user_id=3, game_id=1),
        # gB1
        Player(id=4, position=0, user_id=2, game_id=2),
        Player(id=5, position=1, user_id=1, game_id=2),
        Player(id=6, position=2, user_id=3, game_id=2),
        # gC1
        Player(id=7, position=0, user_id=3, game_id=3),
        Player(id=8, position=1, user_id=1, game_id=3),
        Player(id=9, position=2, user_id=2, game_id=3),
        # gA2
        Player(id=10, position=0, user_id=1, game_id=4),
        Player(id=11, position=1, user_id=2, game_id=4),
    ]
)
ses.add_all(
    [
        # gA1
        Entry(id=1, body="bla", user_id=1, game_id=1),
        Entry(id=2, body="blabla", user_id=2, game_id=1),
        # gC1
        Entry(id=3, body="this is", user_id=3, game_id=3),
        Entry(id=4, body="the end", user_id=1, game_id=3),
    ]
)
ses.commit()
