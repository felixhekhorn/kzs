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


def parse(websocket, msg):
    if msg["type"] == "loadGames":
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
            "myGames": [g.as_dict() for g in myGames],
            "myParticipations": [g.as_dict() for g in myParticipations],
        }
    raise AppError("Unknown type!")


async def handler(websocket, _path):
    async for message in websocket:
        print(f"< {message}")
        response = None
        try:
            msg = json.loads(message)
            if "type" not in msg:
                raise AppError("Invalid request")

            response = parse(websocket, msg)
        except (AppError, KeyError) as e:
            response = {"type": "error", "body": e}

        await websocket.send(json.dumps(response))
        print(f"> {response}")


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    port = int(os.environ.get("PORT", "8001"))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
