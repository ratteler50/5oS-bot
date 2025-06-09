"""Player status management commands (inactive, checkin, etc.)."""
import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send
from utils.player_utils import check_and_print_if_one_or_zero_to_check_in


def backup(filename: str):
    """Import backup function from bot_impl."""
    from bot_impl import backup as backup_impl
    backup_impl(filename)


@registry.command("makeinactive")
async def make_inactive(message: discord.Message, argument: str):
    """Marks a player as inactive."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to make players inactive.")
        return

    from bot_impl import select_player
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    await person.make_inactive()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("undoinactive")
async def undo_inactive(message: discord.Message, argument: str):
    """Marks a player as active."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to make players active.")
        return

    from bot_impl import select_player
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    await person.undo_inactive()
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")


@registry.command("checkin")
async def check_in(message: discord.Message, argument: str):
    """Marks players as checked in."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if global_vars.gamemaster_role not in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to mark a player checked in.")
        return

    from bot_impl import select_player
    people = [
        await select_player(message.author, person, global_vars.game.seatingOrder)
        for person in argument.split(" ")
    ]
    if None in people:
        return
    for person in people:
        person.has_checked_in = True

    await safe_send(message.author, "Successfully marked as checked in: {}".format(
        ", ".join([person.display_name for person in people])))
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")

    await check_and_print_if_one_or_zero_to_check_in()


@registry.command("undocheckin")
async def undo_check_in(message: discord.Message, argument: str):
    """Marks players as not checked in."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if global_vars.gamemaster_role not in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to make players active.")
        return

    from bot_impl import select_player
    people = [
        await select_player(message.author, person, global_vars.game.seatingOrder)
        for person in argument.split(" ")
    ]
    if None in people:
        return

    for person in people:
        person.has_checked_in = False

    await safe_send(message.author, "Successfully marked as not checked in: {}".format(
        ", ".join([person.display_name for person in people])))
    if global_vars.game is not NULL_GAME:
        backup("current_game.pckl")

    await check_and_print_if_one_or_zero_to_check_in()
