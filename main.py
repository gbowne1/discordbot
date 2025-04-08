"""
Main module for the Discord bot.
"""

import os
import logging
import asyncio
from typing import Optional
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class Secrets:
    """
    A class to handle secrets and environment variables.
    """
    @staticmethod
    def get_token() -> Optional[str]:
        """
        Retrieves the Discord bot token from environment variables.
        """
        return os.getenv("DISCORD_TOKEN")

    @classmethod
    def check_env(cls) -> bool:
        """
        Checks if the required environment variables are set.
        """
        token = cls.get_token()
        if not token:
            logger.error("DISCORD_TOKEN is not set in environment variables.")
            return False
        return True
    """
    def get_token() -> Optional[str]:
        """
        Retrieves the Discord bot token from environment variables.
        """
    def check_env(cls) -> bool:
        """
        Checks if the required environment variables are set.
        """
)
logger = logging.getLogger(__name__)

class DiscordBot(commands.Bot):
    """
    Custom Discord bot class with additional functionality.
    """
    @staticmethod
    def get_token() -> Optional[str]:
    async def on_ready(self):
        logger.info("%s has connected to Discord!", self.user.name)
        Event handler for when the bot is ready.
        """

    @classmethod
    def check_env(cls) -> bool:
    async def on_member_join(self, member: disnake.Member):
        logger.info("%s has joined the server.", member)
        Event handler for when a member joins the server.
        """
        if not token:
            logger.warning("Failed to send welcome message to %s: %s", member, e)
            return False
    async def update_member_count(self):
        """
        Periodically updates the member count in a specific channel.
        """

class DiscordBot(commands.Bot):
    def __init__(self):
                logger.info("Updated member count to %d", guild.member_count)
        intents.members = True
                logger.warning("Failed to update member count: %s", e)

    async def on_ready(self):
        logger.info(f"{self.user.name} has connected to Discord!")
def load_extensions(bot: commands.Bot):
    """
    Loads all extensions (cogs) for the bot.
    """
        
        # Start background task to update member count every minute
        asyncio.create_task(self.update_member_count())
                logger.info("Loaded extension: %s", cog_name)
    async def on_member_join(self, member: disnake.Member):
                logger.warning("Extension %s not found.", cog_name)
        try:
                logger.error("No entry point found in extension %s.", cog_name)
            except (commands.ExtensionNotFound, commands.NoEntryPointError, commands.ExtensionFailed) as e:
                logger.error("Failed to load extension %s: %s", cog_name, e, exc_info=True)

async def main():
    """
    Main entry point for the bot.
    """
        while True:
            guild = self.get_guild(123456789)  # Replace with your guild ID
            member_count_channel = guild.get_channel(987654321)  # Replace with your channel ID
            
            try:
                await member_count_channel.edit(name=f"Members: {guild.member_count}")
                logger.info(f"Updated member count to {guild.member_count}")
            except disnake.HTTPException as e:
                logger.warning(f"Failed to update member count: {e}")
            
        logger.error("An error occurred while running the bot: %s", e, exc_info=True)

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

async def main():
    if not Secrets.check_env():
        logger.error("Failed to initialize bot due to missing configuration")
        return

    bot = DiscordBot()
    load_extensions(bot)

    try:
        token = Secrets.get_token()
        await bot.start(token)
    except disnake.LoginFailure:
        logger.error("Invalid token. Please check your DISCORD_TOKEN environment variable.")
    except Exception as e:
        logger.error(f"An error occurred while running the bot: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
