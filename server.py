import asyncio
import json
import os
import signal

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


def serializeGames(games):
    """Prepare data for transfer."""
    gs = {}
    for g in games:
        gg = g.as_dict()
        # add Players + Entries
        gg["players"] = [p.as_dict() for p in g.players]
        gg["entries"] = [e.as_dict() for e in g.entries]
        gs[g.id] = gg
    return gs


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
    users = []
    for g in games:
        for p in g.players:
            if p.user.id not in users:
                users.append(p.user)
    return {
        "type": "loadedGames",
        "games": serializeGames(games),
        "users": {u.id: u.as_dict() for u in users},
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
    new_pos = 1 + len(game.entries)
    e = Entry(user_id=user_id, game_id=game_id, body=msg["body"], position=new_pos)
    ses.add(e)
    ses.commit()
    ses.refresh(e)
    response = {"type": "addEntry", "Entry": e.as_dict()}
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
