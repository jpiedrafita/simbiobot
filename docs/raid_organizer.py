import discord
from discord.ext import commands
from common.logger import logger


class RaidOrganizer(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.events = {}

    @commands.command()
    async def create_event(
        self, ctx, name: str, date: str, time: str, description: str
    ):
        event_message = await ctx.send(
            f"**{name}**\nFecha: {date}\nHora: {time}\n{description}\nÚnete con ✅!"
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
                    f"Participantes en el evento {event_name}: {participants}"
                )
                return
        await ctx.send(f"No se ha encontrado el evento {event_name}")


async def setup(client):
    await client.add_cog(RaidOrganizer(client))
    logger.info("RaidOrganizer loaded")


def setup(client):
    client.add_cog(RaidOrganizer(client))
    logger.info("RaidOrganizer loaded")
