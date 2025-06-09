"""Channel management commands (openpms, closepms, etc.)."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


def backup(filename: str):
    """Import backup function from bot_impl."""
    from bot_impl import backup as backup_impl
    backup_impl(filename)


@registry.command("openpms")
async def open_pms(message: discord.Message, argument: str):
    """Open private messages."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to open PMs.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].open_pms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("opennoms")
async def open_noms(message: discord.Message, argument: str):
    """Open nominations."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to open nominations.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].open_noms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("open", aliases=["openall"])
async def open_all(message: discord.Message, argument: str):
    """Opens pms and nominations"""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to open PMs and nominations.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].open_pms()
    await global_vars.game.days[-1].open_noms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("closepms")
async def close_pms(message: discord.Message, argument: str):
    """Close private messages."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to close PMs.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].close_pms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("closenoms")
async def close_noms(message: discord.Message, argument: str):
    """Close nominations."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to close nominations.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].close_noms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("close", aliases=["closeall"])
async def close_all(message: discord.Message, argument: str):
    """Closes pms and nominations."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to close PMs and nominations.")
        return

    if not global_vars.game.isDay:
        await safe_send(message.author, "It's not day right now.")
        return

    await global_vars.game.days[-1].close_pms()
    await global_vars.game.days[-1].close_noms()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("whispermode")
async def whisper_mode(message: discord.Message, argument: str):
    """Toggle whisper mode."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to change the whispermode.")
        return

    from model.game.whisper_mode import to_whisper_mode
    from utils.game_utils import update_presence
    from bot_client import client

    new_mode = to_whisper_mode(argument)

    if (new_mode):
        global_vars.game.whisper_mode = new_mode
        await update_presence(client)
        for memb in global_vars.gamemaster_role.members:
            await safe_send(memb, "{} has set whisper mode to {}.".format(message.author.display_name,
                                                                          global_vars.game.whisper_mode))
    else:
        await safe_send(message.author,
                        "Invalid whisper mode: {}\nUsage is `@whispermode [all/neighbors/storytellers]`".format(
                            argument))
