import discord
from discord.ext import commands
from localization import get_locale, get_aliases
from config import cfg
from common.logger import logger


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_locales()
        self.aliases = get_aliases(cfg.discord.cogs.ping)

    def update_locales(self):
        self.locale = get_locale(cfg.language, cfg.discord.cogs.ping)

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"*******{__name__} is online!*******")

    @commands.Cog.listener()
    async def on_language_change(self):
        self.update_locales()
        logger.info(f"Language changed to {cfg.language} for {self.__class__.__name__}")

    @commands.command()
    async def ping(self, ctx):
        ping_embed = discord.Embed(
            title="Ping", description=self.locale["latency"], color=discord.Color.blue()
        )
        ping_embed.add_field(
            name=f"{self.bot.user.name}{self.locale['user_latency']}",
            value=f"{round(self.bot.latency * 1000)}ms",
            inline=False,
        )
        ping_embed.set_footer(
            text=f"{self.locale['requested_by']} {ctx.author.name}.",
            icon_url=ctx.author.avatar,
        )
        await ctx.send(embed=ping_embed)
        logger.info("Ping command executed")

    @commands.command(aliases=["hola", "hello", "hi"])
    async def hello_command(self, ctx):
        await ctx.send(self.locale["greeting"])
        logger.info("Hello command executed")
        logger.info(cfg.language)


async def setup(bot):
    await bot.add_cog(Ping(bot))
    logger.info("Ping loaded")
