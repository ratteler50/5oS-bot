"""Utility commands (clear, search, help, etc.)."""
import discord

from commands.registry import registry
from utils import message_utils


@registry.command("clear")
async def clear_channel(message: discord.Message, argument: str):
    """Clear channel messages with whitespace."""
    await message_utils.safe_send(message.author, "{}Clearing\n{}".format("\u200b\n" * 25, "\u200b\n" * 25))


@registry.command("search")
async def search_messages(message: discord.Message, argument: str):
    """Search through message history for a term."""
    import global_vars
    from model.game.game import NULL_GAME
    from bot_impl import get_player

    if global_vars.game is NULL_GAME:
        await message_utils.safe_send(message.author, "There's no game right now.")
        return

    author_roles = global_vars.server.get_member(message.author.id).roles
    if global_vars.gamemaster_role in author_roles or global_vars.observer_role in author_roles:

        history = []
        people = []
        for person in global_vars.game.seatingOrder:
            for msg in person.message_history:
                if not msg["from_player"] in people and not msg["to_player"] in people:
                    history.append(msg)
            people.append(person)

        history = sorted(history, key=lambda i: i["time"])

        message_text = "**Messages mentioning {} (Times in UTC):**\n\n**Day 1:**".format(
            argument
        )
        day = 1
        for msg in history:
            if not (argument.lower() in msg["content"].lower()):
                continue
            while msg["day"] != day:
                await message_utils.safe_send(message.author, message_text)
                day += 1
                message_text = "**Day {}:**".format(str(day))
            message_text += "\nFrom: {} | To: {} | Time: {}\n**{}**".format(
                msg["from_player"].display_name,
                msg["to_player"].display_name,
                msg["time"].strftime("%m/%d, %H:%M:%S"),
                msg["content"],
            )

        await message_utils.safe_send(message.author, message_text)
        return

    if not await get_player(message.author):
        await message_utils.safe_send(message.author, "You are not in the game. You have no message history.")
        return

    message_text = (
        "**Messages mentioning {} (Times in UTC):**\n\n**Day 1:**".format(
            argument
        )
    )
    day = 1
    for msg in (await get_player(message.author)).message_history:
        if not (argument.lower() in msg["content"].lower()):
            continue
        while msg["day"] != day:
            await message_utils.safe_send(message.author, message_text)
            day += 1
            message_text = "**Day {}:**".format(str(day))
        message_text += "\nFrom: {} | To: {} | Time: {}\n**{}**".format(
            msg["from_player"].display_name,
            msg["to_player"].display_name,
            msg["time"].strftime("%m/%d, %H:%M:%S"),
            msg["content"],
        )
    await message_utils.safe_send(message.author, message_text)


@registry.command("makealias")
async def make_alias(message: discord.Message, argument: str):
    """Create a custom command alias."""
    from model.settings.global_settings import GlobalSettings

    argument_parts = argument.split(" ")
    if len(argument_parts) != 2:
        await message_utils.safe_send(message.author,
                                      "makealias takes exactly two arguments: @makealias <alias> <command>")
        return

    global_settings: GlobalSettings = GlobalSettings.load()
    alias_term = argument_parts[0]
    command_term = argument_parts[1]
    if "makealias" == alias_term:
        await message_utils.safe_send(message.author, "Cannot alias the makealias command.")
        return
    global_settings.set_alias(message.author.id, alias_term, command_term)
    global_settings.save()
    await message_utils.safe_send(message.author,
                                  "Successfully created alias {} for command {}.".format(alias_term, command_term))
