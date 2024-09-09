# bot.py

import os
import asyncio
import logging
from typing import Optional

import disnake
from disnake.ext import commands
from decouple import config

from keep_alive import keep_alive

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Secrets:
    @staticmethod
    def get_token() -> Optional[str]:
        return config("TOKEN", default=None)

    @classmethod
    def check_env(cls) -> bool:
        token = cls.get_token()
        if not token:
             logger.error("Environment variable 'TOKEN' is missing")
             return False
        return True

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.all()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        logger.info(f"{self.user.name} has connected to Discord!")
        await self.change_presence(activity=disnake.Game(name="with Discord"))

    async def on_member_join(self, member: disnake.Member):
        logger.info(f"{member} has joined the server.")
        try:
            await member.send(f"Welcome, {member.mention}!")
        except disnake.HTTPException:
            logger.warning(f"Failed to send welcome message to {member}")

        await self.update_member_count(member.guild)

    async def update_member_count(self, guild: disnake.Guild):
        for channel in guild.channels:
            if channel.name.startswith("Members:"):
                try:
                    await channel.edit(name=f"Members: {guild.member_count}")
                    break
                except disnake.HTTPException:
                    logger.warning(f"Failed to update member count in {channel.name}")

def load_extensions(bot: commands.Bot):
    cogs_dir = "./cogs"
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = f"cogs.{filename[:-3]}"
            try:
                bot.load_extension(cog_name)
                logger.info(f"Loaded extension: {cog_name}")
            except commands.ExtensionNotFound:
                logger.warning(f"Extension {cog_name} not found.")
            except commands.NoEntryPointError:
                logger.error(f"No entry point found in extension {cog_name}.")
            except Exception as e:
                logger.error(f"Failed to load extension {cog_name}: {e}", exc_info=True)

def main():
    if not Secrets.check_env():
        logger.error("Failed to initialize bot due to missing configuration")
        return

    bot = DiscordBot()
    load_extensions(bot)
    keep_alive()

    try:
        bot.run(Secrets.get_token())
    except disnake.LoginFailure:
        logger.error("Invalid token. Please check your TOKEN environment variable.")
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}", exc_info=True)

if __name__ == "__main__":
    main()
