# pyright: reportIgnoreCommentWithoutRule=false

import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from socketio import AsyncServer as _AsyncServer
from typing_extensions import Concatenate, ParamSpec

from .quart import quart_app

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AsyncServer(_AsyncServer):  # type: ignore[misc]
    async def emit_error(self, message: str, to: str) -> None:
        await self.emit(
            "server_message", {"message": message, "severity": "ERROR"}, to=to
        )

    async def emit_warning(self, message: str, to: str) -> None:
        await self.emit(
            "server_message", {"message": message, "severity": "WARNING"}, to=to
        )

    async def emit_info(self, message: str, to: str) -> None:
        await self.emit(
            "server_message", {"message": message, "severity": "INFO"}, to=to
        )


sio = AsyncServer(
    logger=logger,  # pyright: ignore[reportArgumentType]
    async_mode="asgi",
)

P = ParamSpec("P")
T = TypeVar("T")
Handler = Callable[Concatenate[str, P], Awaitable[T | None]]


def sio_on(event: str) -> Callable[[Handler[P, T]], Handler[P, T]]:
    def sio_on_decorator(
        handler: Handler[P, T],
    ) -> Handler[P, T]:
        async def wrapped_handler(
            sid: str, /, *args: P.args, **kwargs: P.kwargs
        ) -> T | None:
            async with quart_app.app_context():
                try:
                    logger.debug(
                        f"Received event {event} from {sid} with args {repr(args)}"
                    )
                    return_value = await handler(sid, *args, **kwargs)
                    logger.debug(
                        f"Handler for event {event} from {sid} returned {return_value}"
                    )
                    return return_value
                except Exception as e:
                    await sio.emit_error(str(e), to=sid)
                    logger.exception(e)
                return None

        sio.on(event, wrapped_handler)
        return wrapped_handler

    return sio_on_decorator
