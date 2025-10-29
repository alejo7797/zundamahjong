from socketio import ASGIApp

from . import main as main
from .logger import create_root_logger, create_server_logger
from .quart import quart_app
from .sio import sio

create_root_logger()
create_server_logger(__name__)

app = ASGIApp(sio, quart_app)
