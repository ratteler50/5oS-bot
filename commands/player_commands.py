"""Player management commands (kill, execute, revive, etc.)."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


@registry.command("kill")
async def kill_player(message: discord.Message, argument: str):
    """Kill a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import kill
    await kill(message, argument)


@registry.command("execute")
async def execute_player(message: discord.Message, argument: str):
    """Execute a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import execute
    await execute(message, argument)


@registry.command("exile")
async def exile_player(message: discord.Message, argument: str):
    """Exile a traveler."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import exile
    await exile(message, argument)


@registry.command("revive")
async def revive_player(message: discord.Message, argument: str):
    """Revive a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import revive
    await revive(message, argument)


@registry.command("changerole")
async def change_role(message: discord.Message, argument: str):
    """Change a player's role."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import changerole
    await changerole(message, argument)


@registry.command("changealignment")
async def change_alignment(message: discord.Message, argument: str):
    """Change a player's alignment."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import changealignment
    await changealignment(message, argument)


@registry.command("changeability")
async def change_ability(message: discord.Message, argument: str):
    """Change a player's ability."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import changeability
    await changeability(message, argument)


@registry.command("removeability")
async def remove_ability(message: discord.Message, argument: str):
    """Remove a player's ability."""
    if global_vars.game is NULL_GAME:
        await safe_send(global_vars.channel, "There's no game right now.")
        return

    from bot_impl import removeability
    await removeability(message, argument)
