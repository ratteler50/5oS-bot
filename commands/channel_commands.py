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
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import opennoms
    await opennoms(message, argument)


@registry.command("open", aliases=["openall"])
async def open_all(message: discord.Message, argument: str):
    """Open all channels."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import open_command
    await open_command(message, argument)


@registry.command("closepms")
async def close_pms(message: discord.Message, argument: str):
    """Close private messages."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import closepms
    await closepms(message, argument)


@registry.command("closenoms")
async def close_noms(message: discord.Message, argument: str):
    """Close nominations."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import closenoms
    await closenoms(message, argument)


@registry.command("close", aliases=["closeall"])
async def close_all(message: discord.Message, argument: str):
    """Close all channels."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import close_command
    await close_command(message, argument)


@registry.command("whispermode")
async def whisper_mode(message: discord.Message, argument: str):
    """Toggle whisper mode."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.channel, "There's no game right now.")
        return

    from bot_impl import whispermode
    await whispermode(message, argument)
