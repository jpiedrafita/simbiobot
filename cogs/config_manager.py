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
        self.locale = get_locale(cfg.language, cfg.discord.cogs.config_manager)

    @commands.command()
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
                # await self.update_language("en", reaction.message.channel)
                cfg.language = "en"
            elif reaction.emoji == "🇪🇸":
                # await self.update_language("es", reaction.message.channel)
                cfg.language = "es"

    # TODO: Implementar cambio efectivo de lenguage

    # async def update_language(self, language_code, channel):
    #     # Actualizar el idioma en la configuración y guardar el archivo
    #     cfg["language"] = language_code
    #     with open(self.config_file_path, "w") as config_file:
    #         json.dump(cfg, config_file, indent=4)

    #     # Informar al usuario del cambio
    #     await channel.send(
    #         f"Language changed to {language_code}. Please restart the bot for changes to take effect."
    #     )
    #     logger.info(f"Language changed to {language_code}")


async def setup(bot):
    await bot.add_cog(ConfigManager(bot))
    logger.info("ConfigManager loaded")
