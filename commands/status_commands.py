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


@registry.command("notactive")
async def not_active(message: discord.Message, argument: str):
    """Show players who haven't spoken."""
    from model.player import STORYTELLER_ALIGNMENT

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to view that information.")
        return

    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if global_vars.game.isDay == False:
        await safe_send(message.author, "It's not day right now.")
        return

    notActive = [
        player
        for player in global_vars.game.seatingOrder
        if player.is_active == False and player.alignment != STORYTELLER_ALIGNMENT
    ]

    if notActive == []:
        await safe_send(message.author, "Everyone has spoken!")
        return

    message_text = "These players have not spoken:"
    for player in notActive:
        message_text += "\n{}".format(player.display_name)

    await safe_send(message.author, message_text)


@registry.command("tocheckin")
async def to_check_in(message: discord.Message, argument: str):
    """Show players who haven't checked in."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to view that information.")
        return

    if global_vars.game.isDay:
        await safe_send(message.author, "It's day right now.")
        return

    to_check_in = [
        player
        for player in global_vars.game.seatingOrder
        if player.has_checked_in == False
    ]
    if not to_check_in:
        await safe_send(message.author, "Everyone has checked in!")
        return

    message_text = "These players have not checked in:"
    for player in to_check_in:
        message_text += "\n{}".format(player.display_name)

    await safe_send(message.author, message_text)


@registry.command("cannominate")
async def can_nominate(message: discord.Message, argument: str):
    """Show players who can still nominate."""
    from model.player import STORYTELLER_ALIGNMENT

    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if global_vars.game.isDay == False:
        await safe_send(message.author, "It's not day right now.")
        return

    can_nominate = [
        player
        for player in global_vars.game.seatingOrder
        if player.can_nominate == True
           and player.has_skipped == False
           and player.alignment != STORYTELLER_ALIGNMENT
           and player.is_ghost == False
    ]
    if can_nominate == []:
        await safe_send(message.author, "Everyone has nominated or skipped!")
        return

    message_text = "These players have not nominated or skipped:"
    for player in can_nominate:
        message_text += "\n{}".format(player.display_name)

    await safe_send(message.author, message_text)
