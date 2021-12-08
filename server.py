import asyncio
import json
import os
import signal

import websockets
from sqlalchemy.orm import sessionmaker

from db import Base, Game, User, create_db, engine

# open connection
eng = engine("database.db")
create_db(Base, eng)
Session = sessionmaker(bind=eng)
ses = Session()


async def handler(websocket, path):
    async for message in websocket:
        print(f"< {message}")
        msg = json.loads(message)
        response = None
        if "type" in msg and msg["type"] == "loadGames":
            response = {
                "type": "loadedGames",
                "games": [g.as_dict() for g in ses.query(Game).all()],
            }
        else:
            response = {"type": "error"}

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
