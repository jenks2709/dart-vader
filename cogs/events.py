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
    @app_commands.command(
        name="edit-event",
        description="Edit an existing society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event to edit.",
        title="A new title for the event.",
        description="A new description for the event.",
        location="A new location for the event.",
        start_time="New start time using DD/MM/YYYY HH:MM.",
        end_time="New end time using DD/MM/YYYY HH:MM.",
        signup_deadline=(
            "New signup deadline using DD/MM/YYYY HH:MM."
        ),
        maximum_attendees=(
            "A new maximum number of attendees."
        ),
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def edit_event(
        self,
        interaction: discord.Interaction,
        event_id: int,
        title: str | None = None,
        description: str | None = None,
        location: str | None = None,
        start_time: str | None = None,
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

        if all(
            value is None
            for value in (
                title,
                description,
                location,
                start_time,
                end_time,
                signup_deadline,
                maximum_attendees,
            )
        ):
            await interaction.response.send_message(
                "You must provide at least one field to update.",
                ephemeral=True,
            )
            return

        try:
            parsed_start_time = (
                parse_event_datetime(start_time)
                if start_time is not None
                else None
            )

            parsed_end_time = (
                parse_event_datetime(end_time)
                if end_time is not None
                else None
            )

            parsed_signup_deadline = (
                parse_event_datetime(signup_deadline)
                if signup_deadline is not None
                else None
            )

            event = await self.event_service.edit_event(
                guild_id=interaction.guild_id,
                event_id=event_id,
                title=title,
                description=description,
                location=location,
                start_time=parsed_start_time,
                end_time=parsed_end_time,
                signup_deadline=parsed_signup_deadline,
                maximum_attendees=maximum_attendees,
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

        start_timestamp = int(event.start_time.timestamp())

        embed = discord.Embed(
            title="Event updated",
            description=f"**{event.title}** was updated successfully.",
        )

        embed.add_field(
            name="Event ID",
            value=f"`{event.id}`",
            inline=True,
        )

        embed.add_field(
            name="Start time",
            value=f"<t:{start_timestamp}:F>",
            inline=False,
        )

        embed.add_field(
            name="Location",
            value=event.location,
            inline=False,
        )

        if event.end_time is not None:
            end_timestamp = int(event.end_time.timestamp())

            embed.add_field(
                name="End time",
                value=f"<t:{end_timestamp}:F>",
                inline=False,
            )

        if event.signup_deadline is not None:
            deadline_timestamp = int(
                event.signup_deadline.timestamp()
            )

            embed.add_field(
                name="Signup deadline",
                value=f"<t:{deadline_timestamp}:F>",
                inline=False,
            )

        if event.maximum_attendees is not None:
            embed.add_field(
                name="Maximum attendees",
                value=str(event.maximum_attendees),
                inline=True,
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )
    @app_commands.command(
        name="specific-event",
        description="View the details of a specific society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event to view.",
    )
    @app_commands.guild_only()
    async def view_event(
        self,
        interaction: discord.Interaction,
        event_id: int,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        try:
            event = await self.event_service.get_event(
                guild_id=interaction.guild_id,
                event_id=event_id,
            )

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        start_timestamp = int(event.start_time.timestamp())

        embed = discord.Embed(
            title=event.title,
            description=(
                event.description
                if event.description
                else "No description has been provided."
            ),
        )

        embed.add_field(
            name="Start time",
            value=f"<t:{start_timestamp}:F>\n<t:{start_timestamp}:R>",
            inline=False,
        )

        if event.end_time is not None:
            end_timestamp = int(event.end_time.timestamp())

            embed.add_field(
                name="End time",
                value=f"<t:{end_timestamp}:F>",
                inline=False,
            )

        embed.add_field(
            name="Location",
            value=event.location or "No location specified.",
            inline=False,
        )

        if event.signup_deadline is not None:
            deadline_timestamp = int(
                event.signup_deadline.timestamp()
            )

            embed.add_field(
                name="Signup deadline",
                value=f"<t:{deadline_timestamp}:F>",
                inline=False,
            )

        if event.maximum_attendees is not None:
            embed.add_field(
                name="Maximum attendees",
                value=str(event.maximum_attendees),
                inline=True,
            )

        embed.add_field(
            name="Status",
            value=event.status.value.replace("_", " ").title(),
            inline=True,
        )

        embed.add_field(
            name="Event ID",
            value=f"`{event.id}`",
            inline=True,
        )

        embed.set_footer(
            text=f"Created by Discord user ID {event.created_by_discord_id}"
        )

        await interaction.response.send_message(
            embed=embed,
        )
    @app_commands.command(
        name="delete-event",
        description="Delete an existing society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event to delete.",
        confirm="Confirm that the event should be permanently deleted.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def delete_event(
        self,
        interaction: discord.Interaction,
        event_id: int,
        confirm: bool,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        if not confirm:
            await interaction.response.send_message(
                "Deletion cancelled. Set `confirm` to `True` "
                "to permanently delete the event.",
                ephemeral=True,
            )
            return

        try:
            event = await self.event_service.delete_event(
                guild_id=interaction.guild_id,
                event_id=event_id,
            )

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            (
                f"Event **{event.title}** "
                f"(`{event.id}`) was deleted successfully."
            ),
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