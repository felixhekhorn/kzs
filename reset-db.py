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
ses.add_all([Game(id=1, title="Test", user_id=1, slug="gA1")])
ses.add_all(
    [
        Player(id=1, position=1, user_id=1, game_id=1),
        Player(id=2, position=2, user_id=2, game_id=1),
    ]
)
ses.add_all([Entry(id=1, position=1, body="bla", user_id=1, game_id=1)])
ses.commit()

# check
rs = ses.query(User).all()
for u in rs:
    print(u.name)
    for g in u.games:
        print("\t", g.title)
