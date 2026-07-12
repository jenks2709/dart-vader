import discord
from discord import app_commands
from discord.ext import commands

from services.member_service import (
    MemberAlreadyRegisteredError,
    MemberService,
)


class Members(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        member_service: MemberService,
    ) -> None:
        self.bot = bot
        self.member_service = member_service

    @app_commands.command(
    name="register",
    description="Register yourself as a Nerf Society member.",
    )
    @app_commands.describe(
        first_name="Your first name",
        last_name="Your last name",
    )
    @app_commands.guild_only()
    async def register(
        self,
        interaction: discord.Interaction,
        first_name: str,
        last_name: str,
    ) -> None:
        await interaction.response.defer(ephemeral=True)

        if interaction.guild is None:
            await interaction.followup.send(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        first_name = first_name.strip()
        last_name = last_name.strip()

        if not first_name or not last_name:
            await interaction.followup.send(
                "You must enter both your first name and last name.",
                ephemeral=True,
            )
            return

        display_name = f"{first_name} {last_name}"

        try:
            member = await self.member_service.register_member(
                discord_user_id=interaction.user.id,
                guild_id=interaction.guild.id,
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
            )

        except MemberAlreadyRegisteredError:
            await interaction.followup.send(
                "You are already registered.",
                ephemeral=True,
            )
            return

        if interaction.guild.owner_id == interaction.user.id:
            await interaction.followup.send(
                (
                    f"You have been registered. "
                    "Discord does not allow bots to change the server owner's "
                    "nickname, so you will need to update it manually."
                ),
                ephemeral=True,
            )
            return

        try:
            if isinstance(interaction.user, discord.Member):
                await interaction.user.edit(
                    nick=display_name,
                    reason="Nerf Society registration",
                )

        except discord.Forbidden:
            await interaction.followup.send(
                (
                    f"You have been registered, "
                    "but I do not have permission to change your nickname."
                ),
                ephemeral=True,
            )
            return

        except discord.HTTPException:
            await interaction.followup.send(
                (
                    f"You have been registered, "
                    "but Discord could not update your nickname."
                ),
                ephemeral=True,
            )
            return

        await interaction.followup.send(
            (
                f"You have been registered "
                "and your nickname has been updated."
            ),
            ephemeral=True,
        )

    @register.error
    async def register_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        original = getattr(error, "original", error)

        print(f"Register error: {original!r}")

        try:
            if interaction.response.is_done():
                await interaction.followup.send(
                    "An internal error occurred while registering you.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "An internal error occurred while registering you.",
                    ephemeral=True,
                )

        except discord.NotFound:
            print(
                "Could not send the error message because "
                "the Discord interaction had expired."
            )
async def setup(bot: commands.Bot) -> None:
    member_service = getattr(bot, "member_service", None)

    if member_service is None:
        raise RuntimeError("Member service has not been configured.")

    await bot.add_cog(Members(bot, member_service))

async def cog_app_command_error(
    self,
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
) -> None:
    print(f"Register command error: {error!r}")

    if interaction.response.is_done():
        await interaction.followup.send(
            "An internal error occurred while registering you.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "An internal error occurred while registering you.",
            ephemeral=True,
        )