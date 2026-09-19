import discord
from discord import app_commands
from discord.ext import commands

from services.event_service import EventService, InvalidEventError
from utils.datetime_parser import parse_event_datetime
from models.event_signup import EventSignupStatus
from utils.checks import is_member, is_admin

class EventsCog(commands.Cog):
    def __init__(
        self,
        bot: commands.Bot,
        event_service: EventService,
    ) -> None:
        self.bot = bot
        self.event_service = event_service
    @staticmethod
    def _split_signup_lines(
        lines: list[str],
        maximum_length: int = 1000,
    ) -> list[list[str]]:
        pages: list[list[str]] = []
        current_page: list[str] = []
        current_length = 0

        for line in lines:
            additional_length = len(line)

            if current_page:
                additional_length += 2

            if (
                current_page
                and current_length + additional_length > maximum_length
            ):
                pages.append(current_page)
                current_page = []
                current_length = 0

            current_page.append(line)
            current_length += additional_length

        if current_page:
            pages.append(current_page)

        return pages
    @app_commands.command(
        name="event-signups",
        description="View the signup log for a society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event.",
        include_cancelled="Whether cancelled signups should be included.",
    )
    @app_commands.guild_only()
    @is_admin()
    @app_commands.checks.has_permissions(manage_events=True)
    async def view_event_signups(
        self,
        interaction: discord.Interaction,
        event_id: str,
        include_cancelled: bool = False,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=False,
            )
            return

        await interaction.response.defer(
            ephemeral=False,
        )

        try:
            event, signups, counts = (
                await self.event_service.get_event_signup_log(
                    guild_id=interaction.guild_id,
                    event_id=event_id,
                    include_cancelled=include_cancelled,
                )
            )

        except InvalidEventError as error:
            await interaction.followup.send(
                str(error),
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title=f"Signup log: {event.title}",
            description=f"Event ID: `{event.event_id}`",
        )

        signed_up_count = counts[EventSignupStatus.SIGNED_UP]
        waitlisted_count = counts[EventSignupStatus.WAITLISTED]
        cancelled_count = counts[EventSignupStatus.CANCELLED]
        attended_count = counts[EventSignupStatus.ATTENDED]
        no_show_count = counts[EventSignupStatus.NO_SHOW]

        embed.add_field(
            name="Summary",
            value=(
                f"✅ Signed up: **{signed_up_count}**\n"
                f"⏳ Waitlisted: **{waitlisted_count}**\n"
                f"🎟️ Attended: **{attended_count}**\n"
                f"❌ No-show: **{no_show_count}**\n"
                f"🚫 Cancelled: **{cancelled_count}**"
            ),
            inline=False,
        )

        if event.maximum_attendees is not None:
            remaining_places = max(
                event.maximum_attendees - signed_up_count,
                0,
            )

            embed.add_field(
                name="Capacity",
                value=(
                    f"{signed_up_count}/{event.maximum_attendees} places filled\n"
                    f"{remaining_places} places remaining"
                ),
                inline=False,
            )

        if not signups:
            embed.add_field(
                name="Signup entries",
                value="There are no signups for this event.",
                inline=False,
            )

            await interaction.followup.send(
                embed=embed,
                
            )
            return

        status_icons = {
            EventSignupStatus.SIGNED_UP: "✅",
            EventSignupStatus.WAITLISTED: "⏳",
            EventSignupStatus.CANCELLED: "🚫",
            EventSignupStatus.ATTENDED: "🎟️",
            EventSignupStatus.NO_SHOW: "❌",
        }

        lines: list[str] = []

        for position, signup in enumerate(signups, start=1):
            icon = status_icons.get(signup.status, "•")
            signup_timestamp = int(signup.signup_time.timestamp())

            line = (
                f"{position}. {icon} <@{signup.discord_id}> "
                f"— {signup.status.value.replace('_', ' ').title()}\n"
                f"   Signed up <t:{signup_timestamp}:R>"
            )

            if signup.notes:
                cleaned_notes = signup.notes.replace("\n", " ").strip()

                if len(cleaned_notes) > 100:
                    cleaned_notes = f"{cleaned_notes[:97]}..."

                line += f"\n   Notes: {cleaned_notes}"

            lines.append(line)

        pages = self._split_signup_lines(lines)

        for page_number, page_lines in enumerate(pages, start=1):
            page_embed = embed.copy()

            page_embed.add_field(
                name=(
                    "Signup entries"
                    if len(pages) == 1
                    else f"Signup entries — page {page_number}/{len(pages)}"
                ),
                value="\n\n".join(page_lines),
                inline=False,
            )

            if page_number == 1:
                await interaction.followup.send(
                    embed=page_embed,
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    embed=page_embed,
                    ephemeral=True,
                )
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
                f"🆔 Event ID: `{event.event_id}`",
            ]

            if event.maximum_attendees is not None:
                details.append(
                    f"👥 Maximum attendees: {event.maximum_attendees}"
                )
            details.append(
                f"Sign up: `/signup-event event_id:{event.event_id}`"
            )
            details.append(
                f"🚫 Withdraw: `/withdraw-event event_id:{event.event_id}`"
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
    @is_admin()
    @app_commands.checks.has_permissions(manage_events=True)
    async def create_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
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
                event_id=event_id,
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
    @is_admin()
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
        event_id: str,
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
            value=f"`{event.event_id}`",
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
        event_id: str,
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
            value=f"`{event.event_id}`",
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
    @is_admin()
    @app_commands.describe(
        event_id="The ID of the event to delete.",
        confirm="Confirm that the event should be permanently deleted.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def delete_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
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
                f"(`{event.event_id}`) was deleted successfully."
            ),
            ephemeral=True,
        )
    @app_commands.command(
        name="signup-event",
        description="Sign up for a society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event you want to attend.",
        notes="Optional information about your signup.",
    )
    @app_commands.guild_only()
    @is_member()
    async def signup_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
        notes: str | None = None,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        try:
            signup = await self.event_service.sign_up_for_event(
                guild_id=interaction.guild_id,
                event_id=event_id,
                discord_id=interaction.user.id,
                notes=notes,
            )

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        except ValueError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        if signup.status.value == "waitlisted":
            message = (
                "This event is currently full. "
                "You have been added to the waitlist."
            )
        else:
            message = "You have successfully signed up for the event."

        await interaction.response.send_message(
            message,
            ephemeral=True,
        )
    @app_commands.command(
        name="withdraw-event",
        description="Withdraw your signup from a society event.",
    )
    @app_commands.describe(
        event_id="The ID of the event you want to withdraw from.",
    )
    @app_commands.guild_only()
    async def withdraw_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
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

            await self.event_service.withdraw_from_event(
                guild_id=interaction.guild_id,
                event_id=event_id,
                discord_id=interaction.user.id,
            )

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            (
                f"You have withdrawn from **{event.title}** "
            ),
            ephemeral=True,
        )
    @app_commands.command(
        name="register-attendance",
        description="Register whether a member attended an event.",
    )
    @is_admin()
    @app_commands.describe(
        event_id="The ID of the event.",
        member="The member whose attendance should be recorded.",
        attended="True if they attended, False if they were a no-show.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def register_attendance(
        self,
        interaction: discord.Interaction,
        event_id: str,
        member: discord.Member,
        attended: bool,
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

            await self.event_service.register_event_attendance(
                guild_id=interaction.guild_id,
                event_id=event_id,
                discord_id=member.id,
                attended=attended,
            )

        except InvalidEventError as error:
            await interaction.response.send_message(
                str(error),
                ephemeral=True,
            )
            return

        attendance_text = "attended" if attended else "did not attend"

        await interaction.response.send_message(
            (
                f"Recorded that {member.mention} **{attendance_text}** "
                f"**{event.title}**."
            ),
            ephemeral=True,
        )
    @app_commands.command(
        name="announce-event",
        description="Send an event announcement to a specific channel.",
    )
    @is_admin()
    @app_commands.describe(
        event_id="The ID of the event to announce.",
        channel="The channel where the announcement should be sent.",
        ping_everyone="Whether @everyone should be notified.",
        message="Optional additional announcement message.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def announce_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
        channel: discord.TextChannel,
        ping_everyone: bool = False,
        message: str | None = None,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        if channel.guild.id != interaction.guild_id:
            await interaction.response.send_message(
                "You must select a channel from this server.",
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

        bot_member = channel.guild.me

        if bot_member is None:
            await interaction.response.send_message(
                "I could not check my permissions in that channel.",
                ephemeral=True,
            )
            return

        permissions = channel.permissions_for(bot_member)

        if not permissions.view_channel:
            await interaction.response.send_message(
                "I cannot view the selected channel.",
                ephemeral=True,
            )
            return

        if not permissions.send_messages:
            await interaction.response.send_message(
                "I do not have permission to send messages in that channel.",
                ephemeral=True,
            )
            return

        if not permissions.embed_links:
            await interaction.response.send_message(
                "I need the **Embed Links** permission in that channel.",
                ephemeral=True,
            )
            return

        if ping_everyone and not permissions.mention_everyone:
            await interaction.response.send_message(
                (
                    "I need the **Mention Everyone** permission "
                    "to notify @everyone."
                ),
                ephemeral=True,
            )
            return

        start_timestamp = int(event.start_time.timestamp())

        embed = discord.Embed(
            title=event.title,
            description=(
                event.description
                if event.description
                else "A new society event has been announced."
            ),
        )

        embed.add_field(
            name="Start time",
            value=(
                f"<t:{start_timestamp}:F>\n"
                f"<t:{start_timestamp}:R>"
            ),
            inline=False,
        )

        embed.add_field(
            name="Location",
            value=event.location or "No location specified.",
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

        embed.add_field(
            name="Event ID",
            value=f"`{event.event_id}`",
            inline=True,
        )

        embed.add_field(
            name="Sign up",
            value=f"`/signup-event event_id:{event.event_id}`",
            inline=False,
        )

        embed.add_field(
            name="Withdraw",
            value=f"`/withdraw-event event_id:{event.event_id}`",
            inline=False,
        )

        embed.set_footer(
            text=(
                "Announcement requested by "
                f"{interaction.user.display_name}"
            )
        )

        content_parts: list[str] = []

        if ping_everyone:
            content_parts.append("@everyone")

        if message:
            content_parts.append(message)

        announcement_content = "\n".join(content_parts) or None

        try:
            announcement = await channel.send(
                content=announcement_content,
                embed=embed,
                allowed_mentions=discord.AllowedMentions(
                    everyone=ping_everyone,
                    users=False,
                    roles=False,
                    replied_user=False,
                ),
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                (
                    "Discord blocked the announcement. "
                    "Check my permissions in the selected channel."
                ),
                ephemeral=True,
            )
            return

        except discord.HTTPException:
            await interaction.response.send_message(
                "Discord could not send the announcement.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            (
                f"Announcement sent successfully in {channel.mention}.\n"
                f"[View announcement]({announcement.jump_url})"
            ),
            ephemeral=True,
        )
    @app_commands.command(
        name="remind-event",
        description="Send a reminder for an upcoming event.",
    )
    @is_admin()
    @app_commands.describe(
        event_id="The ID of the event to remind members about.",
        channel="The channel where the reminder should be sent.",
        ping_everyone="Whether @everyone should be notified.",
        message="Optional additional reminder message.",
    )
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_events=True)
    async def remind_event(
        self,
        interaction: discord.Interaction,
        event_id: str,
        channel: discord.TextChannel,
        ping_everyone: bool = False,
        message: str | None = None,
    ) -> None:
        if interaction.guild_id is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True,
            )
            return

        if channel.guild.id != interaction.guild_id:
            await interaction.response.send_message(
                "You must select a channel from this server.",
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

        now = discord.utils.utcnow()

        if event.start_time <= now:
            await interaction.response.send_message(
                "You cannot send a reminder for an event that has already started.",
                ephemeral=True,
            )
            return

        bot_member = channel.guild.me

        if bot_member is None:
            await interaction.response.send_message(
                "I could not check my permissions in that channel.",
                ephemeral=True,
            )
            return

        permissions = channel.permissions_for(bot_member)

        if not permissions.view_channel:
            await interaction.response.send_message(
                "I cannot view the selected channel.",
                ephemeral=True,
            )
            return

        if not permissions.send_messages:
            await interaction.response.send_message(
                "I do not have permission to send messages in that channel.",
                ephemeral=True,
            )
            return

        if not permissions.embed_links:
            await interaction.response.send_message(
                "I need the **Embed Links** permission in that channel.",
                ephemeral=True,
            )
            return

        if ping_everyone and not permissions.mention_everyone:
            await interaction.response.send_message(
                (
                    "I need the **Mention Everyone** permission "
                    "to notify @everyone."
                ),
                ephemeral=True,
            )
            return

        start_timestamp = int(event.start_time.timestamp())

        embed = discord.Embed(
            title=f"Reminder: {event.title}",
            description=(
                event.description
                if event.description
                else "This event is coming up soon."
            ),
        )

        embed.add_field(
            name="Starts",
            value=(
                f"<t:{start_timestamp}:F>\n"
                f"<t:{start_timestamp}:R>"
            ),
            inline=False,
        )

        embed.add_field(
            name="Location",
            value=event.location or "No location specified.",
            inline=False,
        )

        if event.end_time is not None:
            end_timestamp = int(event.end_time.timestamp())

            embed.add_field(
                name="Ends",
                value=f"<t:{end_timestamp}:F>",
                inline=False,
            )

        if event.signup_deadline is not None:
            deadline_timestamp = int(
                event.signup_deadline.timestamp()
            )

            embed.add_field(
                name="Signup deadline",
                value=(
                    f"<t:{deadline_timestamp}:F>\n"
                    f"<t:{deadline_timestamp}:R>"
                ),
                inline=False,
            )

        if event.maximum_attendees is not None:
            embed.add_field(
                name="Maximum attendees",
                value=str(event.maximum_attendees),
                inline=True,
            )

        embed.add_field(
            name="Event ID",
            value=f"`{event.event_id}`",
            inline=True,
        )

        embed.add_field(
            name="Signup commands",
            value=(
                f"✅ `/signup-event event_id:{event.event_id}`\n"
                f"🚫 `/withdraw-event event_id:{event.event_id}`"
            ),
            inline=False,
        )

        embed.set_footer(
            text=(
                "Reminder requested by "
                f"{interaction.user.display_name}"
            )
        )

        content_parts: list[str] = []

        if ping_everyone:
            content_parts.append("@everyone")

        if message:
            content_parts.append(message)

        reminder_content = "\n".join(content_parts) or None

        try:
            reminder = await channel.send(
                content=reminder_content,
                embed=embed,
                allowed_mentions=discord.AllowedMentions(
                    everyone=ping_everyone,
                    users=False,
                    roles=False,
                    replied_user=False,
                ),
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                (
                    "Discord blocked the reminder. "
                    "Check my permissions in the selected channel."
                ),
                ephemeral=True,
            )
            return

        except discord.HTTPException:
            await interaction.response.send_message(
                "Discord could not send the event reminder.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            (
                f"Reminder sent successfully in {channel.mention}.\n"
                f"[View reminder]({reminder.jump_url})"
            ),
            ephemeral=True,
        )
    async def cog_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(
                "You need the Member role to use this command.", ephemeral=True
            )
        elif isinstance(error, app_commands.NoPrivateMessage):
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
        else:
            raise error    
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