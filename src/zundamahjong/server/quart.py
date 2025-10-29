from quart import Quart, redirect, url_for
from werkzeug.wrappers import Response

from ..database import db

quart_app = Quart(
    "zundamahjong", static_url_path="/zundamahjong/", static_folder="client"
)

db.init_app(quart_app)


@quart_app.route("/")
def base() -> Response:
    return redirect(url_for("index"))


@quart_app.route("/zundamahjong/")
def index() -> Response:
    return quart_app.send_static_file("index.html")
