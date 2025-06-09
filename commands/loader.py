"""Command loader to import all command modules."""
import importlib


def load_all_commands():
    """Import all command modules to register their commands."""
    command_modules = [
        "commands.info_commands",
        # "commands.game_commands",  # temporarily disabled
        "commands.player_commands",
        "commands.channel_commands",
        "commands.admin_commands",
        "commands.status_commands",
        "commands.seating_commands",
        "commands.info_status_commands",
        "commands.utility_commands",
        # "commands.voting_commands",  # TODO: enable after implementing
    ]

    for module_name in command_modules:
        importlib.import_module(module_name)
