import discord
from discord.ext import commands
from localization import get_locale, get_aliases
from config import cfg
from common.logger import logger


class EventsOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.locale = get_locale(cfg.language, cfg.discord.cogs.events_organizer)
        self.aliases = get_aliases(cfg.discord.cogs.events_organizer)
        self.events = {}

    @commands.command(aliases=["create", "event", "new", "add", "crear", "evento"])
    async def create_event(
        self, ctx, name: str, date: str, time: str, description: str
    ):
        event_message = await ctx.send(
            f"**{name}**\n{self.locale["date"]} {date}\n{self.locale["time"]} {time}\n{description}\n{self.locale["join_with_reaction"]}"
        )
        await event_message.add_reaction("✅")
        self.events[event_message.id] = {
            "name": name,
            "date": date,
            "time": time,
            "description": description,
            "participants": [],
        }
        logger.info(
            f"Event {event_message.id} created: {self.events[event_message.id]}"
        )

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def event_participants(self, ctx, *, event_name: str):
        for event in self.events.values():
            if event["name"] == event_name:
                participants = [
                    self.client.get_user(user_id).mention
                    for user_id in event["participants"]
                ]
                await ctx.send(
                    f"{self.locale.participants_in_event} {event_name}: {participants}"
                )
                return
        await ctx.send(f"{self.locale.event_not_found}: {event_name}")


async def setup(bot):
    await bot.add_cog(EventsOrganizer(bot))
    logger.info("EvetnsOrganizer loaded")
