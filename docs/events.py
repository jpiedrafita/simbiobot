import discord
from discord.ext import commands
from common.logger import logger


class EventCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.events = {}

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        event_id = reaction.message.id
        if event_id in self.events and reaction.emoji == "✅":
            self.events[event_id]["participants"].append(user.id)
            await reaction.message.channel.send(
                f"{user.mention} se ha unido al evento {self.events[event_id]['name']}"
            )
            logger.info(f"User {user.id} joined event {event_id}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        event_id = reaction.message.id
        if event_id in self.events and reaction.emoji == "✅":
            self.events[event_id]["participants"].remove(user.id)
            await reaction.message.channel.send(
                f"{user.mention} se ha retirado del evento {self.events[event_id]['name']}"
            )
            logger.info(f"User {user.id} left event {event_id}")


async def setup(client):
    await client.add_cog(EventCog(client))
    logger.info("EventCog loaded")


def setup(client):
    client.add_cog(EventCog(client))
    logger.info("EventCog loaded")
