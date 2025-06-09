"""Player information and status commands."""
import inspect

import discord

import global_vars
from commands.registry import registry
from model.game.game import NULL_GAME
from utils.message_utils import safe_send


@registry.command("info")
async def player_info(message: discord.Message, argument: str):
    """Show detailed player information."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to view player information.")
        return

    from bot_impl import select_player
    person = await select_player(
        message.author, argument, global_vars.game.seatingOrder
    )
    if person is None:
        return

    base_info = inspect.cleandoc(f"""
        Player: {person.display_name}
        Character: {person.character.role_name}
        Alignment: {person.alignment}
        Alive: {not person.is_ghost}
        Dead Votes: {person.dead_votes}
        Poisoned: {person.character.is_poisoned}
        Last Active <t:{int(person.last_active)}:R> at <t:{int(person.last_active)}:t>
        Has Checked In {person.has_checked_in}
        ST Channel: {f"https://discord.com/channels/{global_vars.server.id}/{person.st_channel.id}" if person.st_channel else "None"}
        """)

    # Add Hand Status
    hand_status_info = f"Hand Status: {'Raised' if person.hand_raised else 'Lowered'}"

    # Add Preset Vote Status
    preset_vote_info = "Preset Vote: N/A (No active vote)"
    active_vote = None
    if global_vars.game.isDay and global_vars.game.days[-1].votes and not global_vars.game.days[-1].votes[-1].done:
        active_vote = global_vars.game.days[-1].votes[-1]

    if active_vote:
        preset_value = active_vote.presetVotes.get(person.user.id)
        if preset_value is None:
            preset_vote_info = "Preset Vote: None"
        elif preset_value == 0:
            preset_vote_info = "Preset Vote: No"
        elif preset_value == 1:
            preset_vote_info = "Preset Vote: Yes"
        elif preset_value == 2:  # Assuming 2 is for Banshee scream, adjust if needed
            preset_vote_info = "Preset Vote: Yes (Banshee Scream)"
        # Add more conditions if other preset_values are possible

    full_info = "\n".join([base_info, hand_status_info, preset_vote_info, person.character.extra_info()])
    await safe_send(message.author, full_info)


@registry.command("votehistory")
async def vote_history(message: discord.Message, argument: str):
    """Show voting history for all days."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if global_vars.gamemaster_role not in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to view player information.")
        return

    for index, day in enumerate(global_vars.game.days):
        votes_for_day = f"Day {index + 1}\n"
        for vote in day.votes:  # type: Vote
            nominator_name = vote.nominator.display_name if vote.nominator else "the storytellers"
            nominee_name = vote.nominee.display_name if vote.nominee else "the storytellers"
            voters = ", ".join([voter.display_name for voter in vote.voted])
            votes_for_day += f"{nominator_name} -> {nominee_name} ({vote.votes}): {voters}\n"
        await safe_send(message.author, f"```\n{votes_for_day}\n```")


@registry.command("grimoire")
async def grimoire(message: discord.Message, argument: str):
    """Show the grimoire with all player roles."""
    if global_vars.game is NULL_GAME:
        await safe_send(message.author, "There's no game right now.")
        return

    if not global_vars.gamemaster_role in global_vars.server.get_member(message.author.id).roles:
        await safe_send(message.author, "You don't have permission to view player information.")
        return

    message_text = "**Grimoire:**"
    for player in global_vars.game.seatingOrder:
        message_text += "\n{}: {}".format(
            player.display_name, player.character.role_name
        )
        if player.character.is_poisoned and player.is_ghost:
            message_text += " (Poisoned, Dead)"
        elif player.character.is_poisoned and not player.is_ghost:
            message_text += " (Poisoned)"
        elif not player.character.is_poisoned and player.is_ghost:
            message_text += " (Dead)"

    await safe_send(message.author, message_text)
