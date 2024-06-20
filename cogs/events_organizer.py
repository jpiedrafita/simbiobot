import discord
from discord.ext import commands, tasks
from localization import get_locale, get_aliases
from config import cfg
from common.logger import logger
from datetime import datetime, timedelta
import asyncio
from common.helpers import check_time_format, check_date_format


class EventsOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.locale = get_locale(cfg.language, cfg.discord.cogs.events_organizer)
        self.aliases = get_aliases(cfg.discord.cogs.events_organizer)
        self.events = {}

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"*******{__name__} is online!*******")

    @commands.command(aliases=["create", "event", "new", "add", "crear", "evento"])
    async def create_event(
        self, ctx, name: str, description: str, date: str, time: str, capacity: int = 3
    ):
        

        if not check_date_format(date):
            await ctx.send(self.locale["invalid_date"])
            return

        if not check_time_format(time):
            await ctx.send(self.locale["invalid_time"])
            return

        if not isinstance(capacity, int) or capacity <= 0 or capacity > 12:
            await ctx.send(self.locale["invalid_capacity"])
            return

        if capacity <= 3:
            color = discord.Color.yellow()
        elif capacity <= 6:
            color = discord.Color.purple()
        elif capacity <= 12:
            color = discord.Color.red()
        else:
            color = discord.Color.blue()

        # green=ongoing, purple=6, red=12, yellow=3
        embed = discord.Embed(title=name, description=description, color=color)
        embed.add_field(name=self.locale["date"], value=date)
        embed.add_field(name=self.locale["time"], value=time)
        embed.add_field(name=self.locale["capacity"], value=f"0(0)/{capacity}")
        embed.set_footer(text=self.locale["join_with_reaction"])

        if cfg.exists("events_channel_id"):
            event_message = await self.bot.get_channel(cfg.events_channel_id).send(
                embed=embed
            )
            redirect_message = await ctx.send(
            f"**{name}**\n"
            f"{self.locale["date"]} {date}\n"
            f"{self.locale["time"]} {time}\n"
            f"{description}\n"
            f"{self.locale["redirect_message"]} {self.bot.get_channel(cfg.events_channel_id).mention}"
        )
            id = cfg.events_channel_id
        else:
            event_message = await ctx.send(embed=embed)
            id = ctx.channel.id

        await event_message.add_reaction("✅")
        await event_message.add_reaction("🅿️")

        self.events[event_message.id] = {
            "name": name,
            "date": date,
            "time": time,
            "description": description,
            "capacity": capacity,
            "participants": [],
            "substitutes": [],
            "message_id": event_message.id,
            "channel_id": id,
        }

        # # Schedule reminders and cleanup
        # event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        # self.schedule_reminders(event_message.id, event_datetime)
        # self.schedule_cleanup(event_message.id, event_datetime)

        logger.info(
            f"Event {event_message.id} created: {self.events[event_message.id]}"
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def event_participants(self, ctx, *, event_name: str):
        for event in self.events.values():
            if event["name"] == event_name:
                participants = [
                    # self.client.get_user(user_id).mention
                    # for user_id in event["participants"]
                ]
                await ctx.send(
                    f"{self.locale.participants_in_event} {event_name}: {participants}"
                )
                return
        await ctx.send(f"{self.locale.event_not_found}: {event_name}")


async def setup(bot):
    await bot.add_cog(EventsOrganizer(bot))
    logger.info("EvetnsOrganizer loaded")
