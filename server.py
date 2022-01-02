import asyncio
import json
import os
import signal
import secrets

import websockets
from sqlalchemy.orm import sessionmaker

from db import Entry, Game, Player, User, engine

# open connection
eng = engine("database.db")
Session = sessionmaker(bind=eng)
ses = Session()


class AppError(RuntimeError):
    pass


CONNECTIONS = {}


class App:
    def __init__(self, websocket, msg):
        self.websocket = websocket
        self.msg = msg
        self.user_id = None

    async def loadGames(self):
        """Load all relevant games."""
        # load plays
        plays = ses.query(Player).filter(Player.user_id == self.user_id).all()
        # load associated games
        games = []
        for play in plays:
            g = ses.query(Game).filter(Game.id == play.game_id).first()
            games.append(g)
        # load my fellows
        users = {}
        for g in games:
            g.collect_users(users)

        return {
            "type": "loadedGames",
            "games": {g.id: g.serialize_json() for g in games},
            "users": {user_id: u.as_dict() for user_id, u in users.items()},
        }

    async def newGame(self):
        """Create a new game."""
        g = Game(
            title=self.msg["game_title"],
            user_id=self.user_id,
            slug=secrets.token_urlsafe(8),
            state="init",
        )
        g.players.append(Player(user_id=self.user_id, position=0))
        ses.add(g)
        ses.commit()

        return {
            "type": "newGame",
            "games": {g.id: g.serialize_json()},
            "users": {},
        }

    async def addEntry(self):
        game_id = self.msg["game_id"]
        # check we're part
        play = ses.query(Player).filter(
            Player.user_id == self.user_id, Player.game_id == game_id
        )
        if not play:
            raise AppError(f"User {self.user_id} is not part of Game {game_id}")
        # load the actual game
        game = ses.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise AppError("Game not found")
        e = Entry(user_id=self.user_id, game_id=game_id, body=self.msg["body"])
        ses.add(e)
        ses.commit()
        ses.refresh(e)
        # reply with new entry
        response = {
            "type": "addEntry",
            "Entry": e.as_dict(),
            "next_player_user_id": game.nextPlayer().user_id,
        }
        await self.tell_players(game, response)
        return response

    async def tell_players(self, game, response):
        """Propagate the response to all players"""
        for player in game.players:
            if player.user_id == self.user_id:
                continue  # I'm via return
            if player.user_id in CONNECTIONS:
                await CONNECTIONS[player.user_id].send(json.dumps(response))

    async def startGame(self):
        game_id = self.msg["game_id"]
        # check we're the owner part
        game = ses.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise AppError("Game not found!")
        if game.user_id != self.user_id:
            raise AppError(f"User {self.user_id} is does not own Game {game_id}!")
        if len(game.players) < 3:
            raise AppError(f"At least 3 players are required to play!")
        if game.state != "init":
            raise AppError(f"Game is not in init mode!")
        game.state = "running"
        ses.commit()
        # reply with confirmation for everybody
        response = {
            "type": "startedGame",
            "game_id": game.id,
        }
        await self.tell_players(game, response)
        return response

    async def endGame(self):
        game_id = self.msg["game_id"]
        # check we're the owner part
        game = ses.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise AppError("Game not found!")
        if game.user_id != self.user_id:
            raise AppError(f"User {self.user_id} is does not own Game {game_id}!")
        if game.state != "running":
            raise AppError(f"Game is not running!")
        game.state = "finished"
        ses.commit()
        # reply with confirmation for everybody
        response = {
            "type": "endedGame",
            "game_id": game.id,
        }
        await self.tell_players(game, response)
        return response

    async def joinGame(self):
        game_slug = self.msg["game_slug"]
        # check we're the owner part
        game = ses.query(Game).filter(Game.slug == game_slug).first()
        if not game:
            raise AppError("Game not found!")
        if game.state == "finished":
            raise AppError("Game already finished!")
        # check we're not already joined
        play = (
            ses.query(Player)
            .filter(Player.user_id == self.user_id, Player.game_id == game.id)
            .first()
        )
        if play:
            raise AppError(f"User {self.user_id} is already a part of Game {game.id}")
        p = Player(user_id=self.user_id, game_id=game.id, position=len(game.players))
        ses.add(p)
        ses.commit()
        # reply with confirmation for everybody
        users = {}
        game.collect_users(users)
        response = {
            "type": "joinedGame",
            "games": {game.id: game.serialize_json()},
            "users": {user_id: u.as_dict() for user_id, u in users.items()},
        }
        await self.tell_players(game, response)
        return response

    async def login(self):
        """Log a user in."""
        u = (
            ses.query(User)
            .filter(
                User.name == self.msg["user_name"],
                User.password == self.msg["user_password"],
            )
            .first()
        )
        return await self.do_login(u)

    async def do_login(self, u):
        """Register the user in the globale scope and give feedback."""
        if not u:
            raise AppError("Unknown User!")
        # register user
        CONNECTIONS[u.id] = self.websocket
        response = {"type": "loggedIn", "user": u.as_dict()}
        return response

    async def logout(self):
        """Log a user out."""
        # simply unregister
        del CONNECTIONS[self.user_id]

    async def registerUser(self):
        """Register a user via id."""
        # simply register
        u = ses.query(User).filter(User.id == self.user_id).first()
        return await self.do_login(u)

    async def parse(self):
        """Parse a single message."""
        if "type" not in self.msg:
            raise AppError("Invalid request!")
        if self.msg["type"] != "login":
            if "user_id" not in self.msg:
                raise AppError("Unknown User!")
            self.user_id = self.msg["user_id"]
        try:
            f = self.__getattribute__(self.msg["type"])
        except AttributeError:
            raise AppError("Unknown type!")
        return await f()


async def handler(websocket, _path):
    """Handle the stream of messages."""
    async for message in websocket:
        # print(f"< {message}")
        response = None
        try:
            msg = json.loads(message)
            app = App(websocket, msg)
            response = await app.parse()
        except (AppError, KeyError) as e:
            response = {"type": "error", "body": str(e)}

        if response:
            await websocket.send(json.dumps(response))
        # print(f"> {response}")


async def main():
    """Init main event loop on server."""
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
