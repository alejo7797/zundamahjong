from __future__ import annotations

from pydantic import BaseModel, computed_field
from typing_extensions import override


class Player(BaseModel, frozen=True):
    @computed_field  # type: ignore[prop-decorator]
    @property
    def display_name(self) -> str:
        """The player's display name."""
        raise NotImplementedError

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        """Unique id value for the player, for internal use."""
        raise NotImplementedError


class UserPlayer(Player, frozen=True):
    """Pydantic model representing a player as seen by the server."""

    name: str
    """The player's login username (possibly not tied to a permanent
    account)."""

    has_account: bool = False
    """Whether the player has an account on the server.

    Players that choose to set an account password get stored to the database
    and enjoy having the server remember their details over multiple game
    sessions.

    """

    new_user: bool = False
    """Whether the player just created a new account on the server during this
    session."""

    @computed_field  # type: ignore[prop-decorator]
    @property
    @override
    def display_name(self) -> str:
        """The player's display name."""
        return self.name

    @computed_field  # type: ignore[prop-decorator]
    @property
    @override
    def id(self) -> str:
        """Unique id value used internally by :py:mod:`zundamahjong`."""
        return f"player:{self.name}"


class PlayerConnection(BaseModel):
    """Used by :py:class:`.GameRoom` instances to track players in rooms."""

    player: Player
    """Underlying :py:class:`.Player` object that gets tracked."""

    is_connected: bool = True
    """Whether :py:obj:`self.player` is connected to a room or not."""
