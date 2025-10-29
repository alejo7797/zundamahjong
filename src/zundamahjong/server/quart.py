from quart import Quart, redirect, url_for
from quart.wrappers import Response as QResponse
from werkzeug.wrappers import Response

from ..database import db

quart_app = Quart(
    "zundamahjong", static_url_path="/zundamahjong/", static_folder="client"
)

db.init_app(quart_app)


@quart_app.route("/")
async def base() -> Response:
    return redirect(url_for("index"))


@quart_app.route("/zundamahjong/")
async def index() -> QResponse:
    return await quart_app.send_static_file("index.html")
