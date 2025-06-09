"""Information and utility commands (info, time, etc.)."""
import discord

from commands.registry import registry
from utils.message_utils import safe_send


@registry.command("ping")
async def ping_command(message: discord.Message, argument: str):
    """Ping command for testing."""
    await safe_send(message.channel, "Pong!")


@registry.command("test")
async def test_command(message: discord.Message, argument: str):
    """Test command to verify new command system works."""
    await safe_send(message.channel, f"New command system working! Argument: {argument}")
