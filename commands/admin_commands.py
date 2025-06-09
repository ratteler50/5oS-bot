"""Admin/Storyteller commands (welcome, etc.)."""
import discord

import global_vars
from bot_client import client
from commands.registry import registry
from model.channels import ChannelManager
from model.settings import GameSettings
from utils import message_utils


@registry.command("welcome")
async def welcome_player(message: discord.Message, argument: str):
    """Welcomes players to the game with setup instructions."""
    from bot_impl import select_player

    player = await select_player(message.author, argument, global_vars.server.members)
    if player is None:
        return

    if global_vars.gamemaster_role not in global_vars.server.get_member(message.author.id).roles:
        await message_utils.safe_send(message.author, "You don't have permission to do that.")
        return

    bot_nick = global_vars.server.get_member(client.user.id).display_name
    channel_name = global_vars.channel.name
    server_name = global_vars.server.name
    storytellers = [st.display_name for st in global_vars.gamemaster_role.members]

    if len(storytellers) == 1:
        sts = storytellers[0]
    elif len(storytellers) == 2:
        sts = storytellers[0] + " and " + storytellers[1]
    else:
        sts = (
                ", ".join([x for x in storytellers[:-1]])
                + ", and "
                + storytellers[-1]
        )

    game_settings = GameSettings.load()
    st_channel = client.get_channel(game_settings.get_st_channel(player.id))
    if not st_channel:
        st_channel = await ChannelManager(client).create_channel(game_settings, player)
        await message_utils.safe_send(message.author,
                        f'Successfully created the channel https://discord.com/channels/{global_vars.server.id}/{st_channel.id}!')

    await message_utils.safe_send(
        player,
        "Hello, {player_nick}! {storyteller_nick} welcomes you to Blood on the Clocktower on Discord! I'm {bot_nick}, the bot used on #{channel_name} in {server_name} to run games. Your Storyteller channel for this game is #{st_channel}\n\nThis is where you'll perform your private messaging during the game. To send a pm to a player, type `@pm [name]`.\n\nFor more info, type `@help`, or ask the storyteller(s): {storytellers}.".format(
            bot_nick=bot_nick,
            channel_name=channel_name,
            server_name=server_name,
            st_channel=st_channel,
            storytellers=sts,
            player_nick=player.display_name,
            storyteller_nick=global_vars.server.get_member(
                message.author.id
            ).display_name,
        ),
    )
    await message_utils.safe_send(message.author, f'Welcomed {player.display_name} successfully!')
