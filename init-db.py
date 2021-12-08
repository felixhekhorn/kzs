import secrets

from sqlalchemy.orm import sessionmaker

from db import Base, Game, User, create_db, engine

# open connection
eng = engine('database.db')
create_db(Base, eng)
Session = sessionmaker(bind=eng)
ses = Session()

# add initial data
ses.add_all([User(id=1, name='A'),User(id=2, name='B'),])
ses.add_all([Game(id=1, title="Test Game", user_id=1, slug=secrets.token_urlsafe())])
ses.commit()

# check
rs = ses.query(User).all()
for u in rs:
    print(u.name)
    for g in u.games:
        print("\t", g.title)
