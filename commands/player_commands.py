"""Player management commands (kill, execute, revive, etc.)."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


@registry.command("kill")
async def kill_player(message: discord.Message, argument: str):
    """Kills a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to kill players.")
        return

    from bot_impl import select_player, backup
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    if person.is_ghost:
        await safe_send(message.author, "{} is already dead.".format(person.display_name))
        return

    await person.kill(force=True)
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("execute")
async def execute_player(message: discord.Message, argument: str):
    """Executes a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to execute players.")
        return

    from bot_impl import select_player, backup
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    await person.execute(message.author)
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("exile")
async def exile_player(message: discord.Message, argument: str):
    """Exiles a traveler."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to exile travelers.")
        return

    from bot_impl import select_player, backup
    from model.characters import Traveler
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    if not isinstance(person.character, Traveler):
        await safe_send(message.author, "{} is not a traveler.".format(person.display_name))

    await person.character.exile(person, message.author)
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("revive")
async def revive_player(message: discord.Message, argument: str):
    """Revives a player."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to revive players.")
        return

    from bot_impl import select_player, backup
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    if not person.is_ghost:
        await safe_send(message.author, "{} is not dead.".format(person.display_name))
        return

    await person.revive()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")

# TODO: Extract these commands from bot_impl.py elif chain:
# - changerole 
# - changealignment
# - changeability  
# - removeability

# @registry.command("changerole")
# async def change_role(message: discord.Message, argument: str):
#     """Change a player's role."""
#     # Extract logic from bot_impl.py

# @registry.command("changealignment") 
# async def change_alignment(message: discord.Message, argument: str):
#     """Change a player's alignment."""
#     # Extract logic from bot_impl.py

# @registry.command("changeability")
# async def change_ability(message: discord.Message, argument: str):
#     """Change a player's ability."""  
#     # Extract logic from bot_impl.py

# @registry.command("removeability")
# async def remove_ability(message: discord.Message, argument: str):
#     """Remove a player's ability."""
#     # Extract logic from bot_impl.py
