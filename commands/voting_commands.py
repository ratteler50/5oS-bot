"""Voting and nomination commands."""
import discord

from commands.registry import registry


def backup(filename: str):
    """Import backup function from bot_impl."""
    from bot_impl import backup as backup_impl
    backup_impl(filename)


@registry.command("vote")
async def vote(message: discord.Message, argument: str):
    """Cast a vote."""
    # TODO: Extract vote logic from bot_impl.py:1812
    pass


@registry.command("nominate")
async def nominate(message: discord.Message, argument: str):
    """Nominate a player."""
    # TODO: Extract nominate logic from bot_impl.py:1696
    pass


@registry.command("cancelnomination")
async def cancel_nomination(message: discord.Message, argument: str):
    """Cancel a nomination."""
    # TODO: Extract cancelnomination logic from bot_impl.py:1184
    pass


@registry.command("setdeadline")
async def set_deadline(message: discord.Message, argument: str):
    """Set voting deadline."""
    # TODO: Extract setdeadline logic from bot_impl.py:1224
    pass


@registry.command("givedeadvote")
async def give_dead_vote(message: discord.Message, argument: str):
    """Give a dead vote to a player."""
    # TODO: Extract givedeadvote logic from bot_impl.py:1266
    pass


@registry.command("removedeadvote")
async def remove_dead_vote(message: discord.Message, argument: str):
    """Remove a dead vote from a player."""
    # TODO: Extract removedeadvote logic from bot_impl.py:1287
    pass


@registry.command("messagetally")
async def message_tally(message: discord.Message, argument: str):
    """Send tally message."""
    # TODO: Extract messagetally logic from bot_impl.py:1308
    pass


@registry.command("enabletally")
async def enable_tally(message: discord.Message, argument: str):
    """Enable vote tally."""
    # TODO: Extract enabletally logic from bot_impl.py:1403
    pass


@registry.command("disabletally")
async def disable_tally(message: discord.Message, argument: str):
    """Disable vote tally."""
    # TODO: Extract disabletally logic from bot_impl.py:1414
    pass


@registry.command("presetvote", aliases=["prevote"])
async def preset_vote(message: discord.Message, argument: str):
    """Preset a vote."""
    # TODO: Extract presetvote logic from bot_impl.py:1896
    pass


@registry.command("cancelpreset", aliases=["cancelprevote"])
async def cancel_preset(message: discord.Message, argument: str):
    """Cancel preset vote."""
    # TODO: Extract cancelpreset logic from bot_impl.py:2056
    pass


@registry.command("adjustvotes", aliases=["adjustvote"])
async def adjust_votes(message: discord.Message, argument: str):
    """Adjust vote count."""
    # TODO: Extract adjustvotes logic from bot_impl.py:2170
    pass


@registry.command("defaultvote")
async def default_vote(message: discord.Message, argument: str):
    """Set default vote."""
    # TODO: Extract defaultvote logic from bot_impl.py:2194
    pass
