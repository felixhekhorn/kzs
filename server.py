import asyncio
import json
import os
import signal

import websockets
from sqlalchemy.orm import sessionmaker

from db import Base, Game, Player, User, engine

# open connection
eng = engine("database.db")
Session = sessionmaker(bind=eng)
ses = Session()


class AppError(RuntimeError):
    pass


CONNECTIONS = {}

def serializeGames(games):
    """Prepare data for transfer."""
    gs = []
    for g in games:
        gg = g.as_dict()
        # add Players
        ps = []
        for p in g.players:
            pp = p.as_dict()
            pp["user"] = p.user.as_dict()
            ps.append(pp)
        gg["players"] = ps
        # add Entries
        es = []
        for e in g.entries:
            ee = e.as_dict()
            es.append(ee)
        gg["entries"] = es
        gs.append(gg)
    return gs

async def loadGames(websocket, msg):
    """Load all relevant games."""
    user_id = msg["user_id"]
    # register user
    CONNECTIONS[user_id] = websocket
    # as host
    myGames = ses.query(Game).filter(Game.user_id == user_id).all()
    # as player
    myParticipations = (
        ses.query(Game, Player)
        .filter(
            Game.user_id == Player.game_id,
            Player.user_id == user_id,
            Game.user_id != user_id,
        )
        .all()
    )
    myParticipations = [e[0] for e in myParticipations]
    return {
        "type": "loadedGames",
        "myGames": serializeGames(myGames),
        "myParticipations": serializeGames(myParticipations),
    }

async def parse(websocket, msg):
    """Parse a single message."""
    if msg["type"] == "loadGames":
        return await loadGames(websocket, msg)
    raise AppError("Unknown type!")


async def handler(websocket, _path):
    """Handle the stream of messages."""
    async for message in websocket:
        print(f"< {message}")
        response = None
        try:
            msg = json.loads(message)
            if "type" not in msg:
                raise AppError("Invalid request")

            response = await parse(websocket, msg)
        except (AppError, KeyError) as e:
            response = {"type": "error", "body": e}

        if (response):
            await websocket.send(json.dumps(response))
        print(f"> {response}")


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
