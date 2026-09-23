<<<<<<< HEAD
import logging

import discord

logger = logging.getLogger(__name__)


async def shutdown_bot(bot: discord.Client, requested_by: discord.abc.User) -> None:
    """
    Cleanly shut down the bot.

    Any final cleanup, database closing, or state saving should happen here.
    """
    logger.warning(
        "Bot shutdown requested by %s (%s)",
        requested_by,
        requested_by.id,
    )

    #Include any clean up here (i.e. database or state saving)
=======
import logging

import discord

logger = logging.getLogger(__name__)


async def shutdown_bot(bot: discord.Client, requested_by: discord.abc.User) -> None:
    """
    Cleanly shut down the bot.

    Any final cleanup, database closing, or state saving should happen here.
    """
    logger.warning(
        "Bot shutdown requested by %s (%s)",
        requested_by,
        requested_by.id,
    )

    #Include any clean up here (i.e. database or state saving)
>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
    await bot.close()