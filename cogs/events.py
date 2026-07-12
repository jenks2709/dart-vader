import discord
from discord import app_commands
from discord.ext import commands

from services.event_service import EventService, InvalidEventError
from utils.datetime_parser import parse_event_datetime


class EventsCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        event_service: EventService,
    ) -> None:
        self.bot = bot
        self.event_service = event_service

    @app_commands.command(
        name="events",
        description="View upcoming society events.",
    )
    @app_commands.guild_only()
    async def view_events(
        self,
        interaction: discord.Interaction,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        events = await self.event_service.list_upcoming_events(
            guild_id=interaction.guild_id,
            limit=10,
        )

        if not events:
            await interaction.response.send_message(
                "There are currently no upcoming events.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="Upcoming Events",
            description="The next scheduled society events.",
        )

        for event in events:
            start_timestamp = int(event.start_time.timestamp())

            details = [
                f"📅 <t:{start_timestamp}:F>",
                f"📍 {event.location}",
                f"🆔 Event ID: `{event.id}`",
            ]

            if event.maximum_attendees is not None:
                details.append(
                    f"👥 Maximum attendees: {event.maximum_attendees}"
                )

            if event.description:
                details.append(event.description)

            embed.add_field(
                name=event.title,
                value="\n".join(details),
                inline=False,
            )

        await interaction.response.send_message(
            embed=embed,
        )
    @app_commands.command(
        name="create-event",
        description="Create a new society event.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def create_event(
        self,
        interaction: discord.Interaction,
        title: str,
        start_time: str,
        location: str,
        description: str = "",
        end_time: str | None = None,
        signup_deadline: str | None = None,
        maximum_attendees: int | None = None,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        try:
            parsed_start = parse_event_datetime(start_time)
            parsed_end = (
                parse_event_datetime(end_time)
                if end_time
                else None
            )
            parsed_deadline = (
                parse_event_datetime(signup_deadline)
                if signup_deadline
                else None
            )

            event = await self.event_service.create_event(
                guild_id=interaction.guild_id,
                title=title,
                description=description,
                location=location,
                start_time=parsed_start,
                end_time=parsed_end,
                signup_deadline=parsed_deadline,
                maximum_attendees=maximum_attendees,
                created_by_discord_id=interaction.user.id,
            )

        except ValueError:
            await interaction.response.send_message(
                "Invalid date or time. Use `DD/MM/YYYY HH:MM`.",
                ephemeral=True,
            )
            return

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Event **{event.title}** created successfully.",
            ephemeral=True,
        )


async def setup(bot: commands.Bot) -> None:
    event_service = getattr(bot, "event_service", None)

    if event_service is None:
        raise RuntimeError("Event service has not been configured.")

    await bot.add_cog(
        EventsCog(
            bot=bot,
            event_service=event_service,
        )
    )