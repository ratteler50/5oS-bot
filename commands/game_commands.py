"""Game management commands (startgame, endgame, etc.)."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


@registry.command("startgame")
async def start_game(message: discord.Message, argument: str):
    """Start a new game."""
    if global_vars.game is not NULL_GAME:
        await safe_send(global_vars.channel, "There's already a game going on.")
        return

    # Import here to avoid circular imports
    from bot_impl import startgame
    await startgame(message, argument)


@registry.command("endgame")
async def end_game(message: discord.Message, argument: str):
    """End the current game."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import endgame
    await endgame(message, argument)


@registry.command("startday")
async def start_day(message: discord.Message, argument: str):
    """Start a new day."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import startday
    await startday(message, argument)


@registry.command("endday")
async def end_day(message: discord.Message, argument: str):
    """End the current day."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import endday
    await endday(message, argument)
