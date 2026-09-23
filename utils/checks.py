<<<<<<< HEAD
import discord
from discord import app_commands

from config.settings import settings  # adjust to wherever your settings object lives


def is_member():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            raise app_commands.NoPrivateMessage()

        role_id = settings.member_role_id
        if role_id is None:
            raise RuntimeError("MEMBER_ROLE_ID is not set in .env")

        if interaction.user.get_role(role_id) is not None:
            return True

        raise app_commands.MissingRole(role_id)

    return app_commands.check(predicate)

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            raise app_commands.NoPrivateMessage()

        role_id = settings.admin_role_id
        if role_id is None:
            raise RuntimeError("MEMBER_ROLE_ID is not set in .env")

        if interaction.user.get_role(role_id) is not None:
            return True

        raise app_commands.MissingRole(role_id)

=======
import discord
from discord import app_commands

from config.settings import settings  # adjust to wherever your settings object lives


def is_member():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            raise app_commands.NoPrivateMessage()

        role_id = settings.member_role_id
        if role_id is None:
            raise RuntimeError("MEMBER_ROLE_ID is not set in .env")

        if interaction.user.get_role(role_id) is not None:
            return True

        raise app_commands.MissingRole(role_id)

    return app_commands.check(predicate)

def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            raise app_commands.NoPrivateMessage()

        role_id = settings.admin_role_id
        if role_id is None:
            raise RuntimeError("MEMBER_ROLE_ID is not set in .env")

        if interaction.user.get_role(role_id) is not None:
            return True

        raise app_commands.MissingRole(role_id)

>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
    return app_commands.check(predicate)