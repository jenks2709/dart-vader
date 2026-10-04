import asyncio

import discord
from discord.ext import commands

from config.settings import DatabaseConfig, settings
from repositories.event_repository import EventRepository
from repositories.member_repository import MemberRepository
from services.database_service import DatabaseService
from services.event_service import EventService
from services.member_service import MemberService
from utils.logger import logger


INITIAL_EXTENSIONS = (
    "cogs.general",
    "cogs.admin",
    "cogs.members",
    "cogs.events",
)


class DartVaderBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.database = DatabaseService(DatabaseConfig)

        self.member_service: MemberService | None = None
        self.event_service: EventService | None = None

    async def on_interaction(
        self,
        interaction: discord.Interaction,
    ) -> None:
        logger.info(
            "Received interaction: type=%s name=%s user=%s guild=%s",
            interaction.type,
            interaction.data.get("name")
            if interaction.data
            else None,
            interaction.user.id,
            interaction.guild_id,
        )

        await super().on_interaction(interaction)

    async def setup_hook(self) -> None:
        """Initialise services, load extensions, and synchronise commands."""

        await self.database.connect()
        await self.database.initialise()

        if self.database.connection is None:
            raise RuntimeError(
                "Database connection was not established."
            )

        member_repository = MemberRepository(
            self.database.connection
        )

        self.member_service = MemberService(
            member_repository
        )

        event_repository = EventRepository(
            self.database.connection
        )

        self.event_service = EventService(
            event_repository
        )

        for extension in INITIAL_EXTENSIONS:
            try:
                await self.load_extension(extension)
                logger.info("Loaded extension: %s", extension)
            except Exception:
                logger.exception(
                    "Failed to load extension: %s",
                    extension,
                )
                raise

        async def command_error(
            interaction: discord.Interaction,
            error: discord.app_commands.AppCommandError,
        ) -> None:
            original = getattr(error, "original", error)

            logger.error(
                "Application command failed: %r",
                original,
                exc_info=(
                    type(original),
                    original,
                    original.__traceback__,
                ),
            )

            message = (
                "An internal error occurred while running this command."
            )

            if interaction.response.is_done():
                await interaction.followup.send(
                    message,
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    message,
                    ephemeral=True,
                )

        self.tree.on_error = command_error

        if settings.guild_id is not None:
            guild = discord.Object(id=settings.guild_id)

            self.tree.copy_global_to(guild=guild)

            commands_synced = await self.tree.sync(
                guild=guild
            )

            for command in commands_synced:
                logger.info(
                    "Synced command: /%s | application ID: %s",
                    command.name,
                    self.application_id,
                )

            logger.info(
                "Synchronised %d commands to development guild %d",
                len(commands_synced),
                settings.guild_id,
            )
        else:
            commands_synced = await self.tree.sync()

            logger.info(
                "Synchronised %d global commands",
                len(commands_synced),
            )

    async def close(self) -> None:
        """Close external resources before shutting down."""

        await self.database.close()
        await super().close()

    async def on_ready(self) -> None:
        if self.user is None:
            return

        logger.info(
            "Dart Vader is online as %s (%d)",
            self.user,
            self.user.id,
        )


async def main() -> None:
    bot = DartVaderBot()

    try:
        async with bot:
            await bot.start(settings.discord_token)
    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception:
        logger.exception("Dart Vader stopped unexpectedly.")
        raise
    finally:
        logger.info("Dart Vader has shut down.")


if __name__ == "__main__":
    asyncio.run(main())