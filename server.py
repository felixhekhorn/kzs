import asyncio
import json
import os
import signal
import secrets

import websockets
from sqlalchemy.orm import sessionmaker

from db import Entry, Game, Player, engine

# open connection
eng = engine("database.db")
Session = sessionmaker(bind=eng)
ses = Session()


class AppError(RuntimeError):
    pass


CONNECTIONS = {}


async def loadGames(websocket, msg):
    """Load all relevant games."""
    user_id = msg["user_id"]
    # register user
    CONNECTIONS[user_id] = websocket
    # load plays
    plays = ses.query(Player).filter(Player.user_id == user_id).all()
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


async def newGame(websocket, msg):
    """Load all relevant games."""
    user_id = msg["user_id"]
    g = Game(
        title=msg["game_title"],
        user_id=user_id,
        slug=secrets.token_urlsafe(8),
        state="init",
    )
    g.players.append(Player(user_id=user_id, position=0))
    ses.add(g)
    ses.commit()

    return {
        "type": "newGame",
        "games": {g.id: g.serialize_json()},
        "users": {},
    }


async def addEntry(websocket, msg):
    game_id = msg["game_id"]
    user_id = msg["user_id"]
    # check we're part
    play = ses.query(Player).filter(
        Player.user_id == user_id, Player.game_id == game_id
    )
    if not play:
        raise AppError(f"User {user_id} is not part of Game {game_id}")
    # load the actual game
    game = ses.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise AppError("Game not found")
    e = Entry(user_id=user_id, game_id=game_id, body=msg["body"])
    ses.add(e)
    ses.commit()
    ses.refresh(e)
    # reply with new entry
    response = {
        "type": "addEntry",
        "Entry": e.as_dict(),
        "next_player_user_id": game.nextPlayer().user_id,
    }
    for player in game.players:
        if player.user_id == user_id:
            continue  # I'm via return
        if player.user_id in CONNECTIONS:
            await CONNECTIONS[player.user_id].send(json.dumps(response))
    return response


async def startGame(websocket, msg):
    game_id = msg["game_id"]
    user_id = msg["user_id"]
    # check we're the owner part
    game = ses.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise AppError("Game not found!")
    if game.user_id != user_id:
        raise AppError(f"User {user_id} is does not own Game {game_id}!")
    if len(game.players) < 3:
        raise AppError(f"At least 3 players are required to play!")
    game.state = "running"
    ses.commit()
    # reply with confirmation for everybody
    response = {
        "type": "startedGame",
        "game_id": game.id,
    }
    for player in game.players:
        if player.user_id == user_id:
            continue  # I'm via return
        if player.user_id in CONNECTIONS:
            await CONNECTIONS[player.user_id].send(json.dumps(response))
    return response


async def joinGame(websocket, msg):
    game_slug = msg["game_slug"]
    user_id = msg["user_id"]
    # check we're the owner part
    game = ses.query(Game).filter(Game.slug == game_slug).first()
    if not game:
        raise AppError("Game not found!")
    if game.state == "finished":
        raise AppError("Game already finished!")
    # check we're not already joined
    play = (
        ses.query(Player)
        .filter(Player.user_id == user_id, Player.game_id == game.id)
        .first()
    )
    if play:
        raise AppError(f"User {user_id} is already a part of Game {game.id}")
    p = Player(user_id=user_id, game_id=game.id, position=len(game.players))
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
    for player in game.players:
        if player.user_id == user_id:
            continue  # I'm via return
        if player.user_id in CONNECTIONS:
            await CONNECTIONS[player.user_id].send(json.dumps(response))
    return response


async def parse(websocket, msg):
    """Parse a single message."""
    if msg["type"] == "loadGames":
        return await loadGames(websocket, msg)
    if msg["type"] == "addEntry":
        return await addEntry(websocket, msg)
    if msg["type"] == "startGame":
        return await startGame(websocket, msg)
    if msg["type"] == "joinGame":
        return await joinGame(websocket, msg)
    if msg["type"] == "newGame":
        return await newGame(websocket, msg)
    raise AppError("Unknown type!")


async def handler(websocket, _path):
    """Handle the stream of messages."""
    async for message in websocket:
        # print(f"< {message}")
        response = None
        try:
            msg = json.loads(message)
            if "type" not in msg:
                raise AppError("Invalid request")

            response = await parse(websocket, msg)
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
