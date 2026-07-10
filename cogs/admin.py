import logging

import discord
from discord import app_commands
from discord.ext import commands

from services.shutdown import shutdown_bot

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="shutdown",
        description="Safely shut down Dart Vader.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def shutdown(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(
            "Dart Vader is shutting down.",
            ephemeral=True,
        )

        await shutdown_bot(
            bot=self.bot,
            requested_by=interaction.user,
        )

    @shutdown.error
    async def shutdown_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            message = "You must be a server administrator to shut down the bot."
        else:
            logger.exception("Shutdown command failed", exc_info=error)
            message = "The shutdown command failed."

        if interaction.response.is_done():
            await interaction.followup.send(message, ephemeral=True)
        else:
            await interaction.response.send_message(message, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))