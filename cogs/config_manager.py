import discord
from discord.ext import commands
from localization import get_locale, get_aliases
from config import cfg
from common.logger import logger
import json


class ConfigManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_file_path = f"{cfg.config_path}/{cfg.config_file.common}"
        self.update_locales()

    def update_locales(self):
        self.locale = get_locale(cfg.language, cfg.discord.cogs.config_manager)

    @commands.command(aliases=["language", "lang", "idioma"])
    @commands.has_permissions(administrator=True)
    async def change_language(self, ctx):
        # Crear un embed con las opciones de idioma
        embed = discord.Embed(
            title=self.locale["change_language"],
            description=self.locale["language_description"],
            color=discord.Color.blue(),
        )
        embed.add_field(name="Languages", value="🇬🇧 English\n🇪🇸 Español")
        message = await ctx.send(embed=embed)

        # Añadir reacciones para los idiomas
        await message.add_reaction("🇬🇧")
        await message.add_reaction("🇪🇸")

        # Guardar el ID del mensaje y del canal para verificarlo en el evento de reacción
        self.language_change_message_id = message.id
        self.language_change_channel_id = ctx.channel.id

    @commands.command(aliases=["canal_eventos"])
    async def set_event_channel(self, ctx, channel: discord.TextChannel):
        cfg.events_channel_id = channel.id
        cfg.events_channel = channel.name
        # await ctx.send(f"Event channel has been set to {channel.mention}")
        await ctx.send(f"{self.locale["channel_changed"]}{channel.mention}")
        logger.info(f"Event channel has been set to: {channel.name} - {channel.id}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.message.id == getattr(
            self, "language_change_message_id", None
        ) and reaction.message.channel.id == getattr(
            self, "language_change_channel_id", None
        ):
            if reaction.emoji == "🇬🇧":
                cfg.language = "en"
                self.update_locales()
                self.bot.dispatch("language_change")
                await reaction.message.channel.send(
                    self.locale["language_changed"].format(language="English")
                )
            elif reaction.emoji == "🇪🇸":
                cfg.language = "es"
                self.update_locales()
                self.bot.dispatch("language_change")
                await reaction.message.channel.send(
                    self.locale["language_changed"].format(language="Español")
                )


async def setup(bot):
    await bot.add_cog(ConfigManager(bot))
    logger.info("ConfigManager loaded")
