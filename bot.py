import discord
from discord.ext import commands
from config import cfg
from common.logger import logger

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=cfg.discord.prefix, intents=intents)

@client.event
async def on_ready():
    print('Bot is ready.')
    print('-------------')
    

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def hello(ctx):
    await ctx.send('Hola, soy Minola!')
    logger.info("Hello command executed")

client.run(cfg.discord.token)