import discord
import os
import asyncio
from discord.ext import commands
from config import cfg
from common.logger import logger

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(
    command_prefix=cfg.discord.prefix, intents=intents, help_command=None
)


@bot.event
async def on_ready():
    print("Bot is ready.\n-------------")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(cfg.discord.token)


asyncio.run(main())
