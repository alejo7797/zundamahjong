from time import sleep

from .action import Action
from .info import AllGameInfo


def calculate_bot_action(info: AllGameInfo) -> Action:
    """
    Given info on the bot's view of the game state,
    returns the action the bot chooses.

    :param info: An object with the info of the game state from the bot's point of view.
    """

    if len(info.player_info.actions) > 1:
        sleep(0.5)
    return info.player_info.actions[0]
