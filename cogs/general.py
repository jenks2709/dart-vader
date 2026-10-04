import discord
from discord import app_commands
from discord.ext import commands

from utils.logger import logger
from utils.checks import is_admin

class General(commands.Cog):
    """General member-facing commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="ping",
        description="Check whether Dart Vader is online.",
    )
    @is_admin()
    async def ping(
        self,
        interaction: discord.Interaction,
    ) -> None:
        latency_ms = round(self.bot.latency * 1000)

        logger.info(
            "Ping command used by user %s in guild %s",
            interaction.user.id,
            interaction.guild_id,
        )

        await interaction.response.send_message(
            f"Dart Vader is online. Latency: {latency_ms} ms.",
            ephemeral=True,
        )

    @app_commands.command(
        name="vader",
        description="Receive some questionable wisdom from Dart Vader.",
    )
    async def vader(
        self,
        interaction: discord.Interaction,
    ) -> None:
        await interaction.response.send_message(
            "I find your lack of eye protection disturbing."
        )

    @app_commands.command(
        name="about",
        description="Learn what Dart Vader is used for.",
    )
    async def about(
        self,
        interaction: discord.Interaction,
    ) -> None:
        embed = discord.Embed(
            title="Dart Vader",
            description=(
                "Dart Vader supports the day-to-day administration "
                "of the Nerf society."
                " Events, attendance, roles, reminders and general "
                "society administration."
            ),
        )

        embed.add_field(
            name="Tagger",
            value=(
                "Dedicated Humans versus Zombies gameplay systems."
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))