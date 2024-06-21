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
        embed.add_field(name=self.locale["capacity"], value=f"1(0)/{capacity}")
        embed.add_field(name=self.locale["creator"], value=ctx.author.display_name)
        embed.add_field(name=self.locale["players"], value=ctx.author.display_name)
        embed.add_field(name=self.locale["substitutes"], value="")
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

        await event_message.add_reaction(cfg.discord.events_organizer.participants_emoji)
        await event_message.add_reaction(cfg.discord.events_organizer.substitutes_emoji)

        # TODO: Schedule reminders and cleanup
        # event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        # self.schedule_reminders(event_message.id, event_datetime)
        # self.schedule_cleanup(event_message.id, event_datetime)

        logger.info(
            f"Event {event_message.id} created: "
        )


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.message.embeds:
            embed = reaction.message.embeds[0]
            if embed.footer.text == self.locale["join_with_reaction"]:
                print("Adding reaction")
                await self.update_event_participants(reaction, user)


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        print(f"reaction: {reaction}\nuser: {user}\n")
        if user.bot:
            return
        if reaction.message.embeds:
            embed = reaction.message.embeds[0]
            if embed.footer.text == self.locale["join_with_reaction"]:
                print("Removing reaction")
                await self.update_event_participants(reaction, user)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        print(f"Removing RAW reaction {payload}")
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print(f"Adding RAW reaction {payload}")

    # WARNING: events on_reaction_add/remove are not triggered by the event creator user
    async def update_event_participants(self, reaction, user):
        message = reaction.message
        embed = message.embeds[0]
        capacity_field = next(field for field in embed.fields if field.name == self.locale["capacity"])
        players_field = next(field for field in embed.fields if field.name == self.locale["players"])
        substitutes_field = next(field for field in embed.fields if field.name == self.locale["substitutes"])
        capacity = int(capacity_field.value.split('/')[1])
        players = players_field.value.split('\n') if players_field.value else []
        substitutes = substitutes_field.value.split('\n') if substitutes_field.value else []

        print("Reaction: ", reaction.emoji)
        print("user:", user.display_name)


        if reaction.emoji == cfg.discord.events_organizer.participants_emoji:
            if user.display_name in players:
                players.remove(user.display_name)
            elif len(players) < capacity:
                players.append(user.display_name)
                if user.display_name in substitutes:
                    substitutes.remove(user.display_name)
        
        if reaction.emoji == cfg.discord.events_organizer.substitutes_emoji:
            if user.display_name in substitutes:
                substitutes.remove(user.display_name)
            elif len(substitutes) < cfg.discord.events_organizer.max_substitutes:
                substitutes.append(user.display_name)
                if user.display_name in players:
                    players.remove(user.display_name)

        embed.set_field_at(
            embed.fields.index(players_field),
            name=self.locale["players"],
            value="\n".join(players) if players else ""
        )
        embed.set_field_at(
            embed.fields.index(substitutes_field),
            name=self.locale["substitutes"],
            value="\n".join(substitutes) if substitutes else ""
        )
        embed.set_field_at(
            embed.fields.index(capacity_field),
            name=self.locale["capacity"],
            value=f"{len(players)}({len(substitutes)})/{capacity}"
        )
        await message.edit(embed=embed)

 


async def setup(bot):
    await bot.add_cog(EventsOrganizer(bot))
    logger.info("EvetnsOrganizer loaded")
