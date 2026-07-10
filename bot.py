import asyncio

import discord
from discord.ext import commands

from config.settings import settings
from utils.logger import logger


INITIAL_EXTENSIONS = (
    "cogs.general",
    "cogs.admin",
)


class DartVaderBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()

        super().__init__(
            command_prefix="!",
            intents=intents,
        )

    async def setup_hook(self) -> None:
        """Load extensions and synchronise application commands."""

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

        if settings.guild_id is not None:
            guild = discord.Object(id=settings.guild_id)

            self.tree.copy_global_to(guild=guild)
            commands_synced = await self.tree.sync(guild=guild)

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