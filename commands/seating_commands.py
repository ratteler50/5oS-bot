"""Seating and traveler management commands."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


def backup(filename: str):
    """Import backup function from bot_impl."""
    from bot_impl import backup as backup_impl
    backup_impl(filename)


@registry.command("removetraveler", aliases=["removetraveller"])
async def remove_traveler(message: discord.Message, argument: str):
    """Remove a traveler from the game."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to remove travelers.")
        return

    from bot_impl import select_player
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    await global_vars.game.remove_traveler(person)
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("resetseats")
async def reset_seats(message: discord.Message, argument: str):
    """Resets the seating chart."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to change the seating chart.")
        return

    await global_vars.game.reseat(global_vars.game.seatingOrder)
