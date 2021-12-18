# import secrets

from sqlalchemy.orm import sessionmaker

from db import Base, Game, User, Player, Entry, engine

# open connection

eng = engine("database.db")
Base.metadata.drop_all(bind=eng)
Base.metadata.create_all(bind=eng)
Session = sessionmaker(bind=eng)
ses = Session()

# add initial data
ses.add_all(
    [
        User(id=1, name="A"),
        User(id=2, name="B"),
        User(id=3, name="C"),
    ]
)
ses.add_all(
    [
        Game(id=1, title="A1", user_id=1, slug="gA1"),
        Game(id=2, title="B1", user_id=2, slug="gB1"),
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
    ]
)
ses.add_all(
    [
        Entry(id=1, body="bla", user_id=1, game_id=1),
        Entry(id=2, body="blabla", user_id=2, game_id=1),
    ]
)
ses.commit()
