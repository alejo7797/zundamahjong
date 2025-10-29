# pyright: reportAny=false

import argparse
import os
from importlib.metadata import version

import uvicorn

parser = argparse.ArgumentParser(
    prog="zundamahjong", description="Web-based Mahjong game server"
)

parser.add_argument("-p", "--port", type=int, help="port on which to listen")

parser.add_argument(
    "--debug", action="store_true", help="run server in development mode"
)


def main() -> None:
    args = parser.parse_args()

    if args.port is None:
        port = int(os.getenv("DEBUG_SERVER_PORT", 5000))

    else:
        port = args.port

    print(f"Starting Zundamahjong server version {version('zundamahjong')}.")
    print(f"Go to http://localhost:{port} to play some Mahjong.")

    uvicorn.run(
        "zundamahjong.server:app",
        host="localhost",
        port=port,
        reload=args.debug,
        log_config={"version": 1},
    )


if __name__ == "__main__":
    main()
