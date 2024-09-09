# bot.py

import os
import logging
from typing import Optional
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import asyncio

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Secrets:
    @staticmethod
    def get_token() -> Optional[str]:
        return os.getenv("DISCORD_TOKEN")

    @classmethod
    def check_env(cls) -> bool:
        token = cls.get_token()
        if not token:
            logger.error("Environment variable 'DISCORD_TOKEN' is missing")
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
        
        # Start background task to update member count every minute
        asyncio.create_task(self.update_member_count())

    async def on_member_join(self, member: disnake.Member):
        logger.info(f"{member} has joined the server.")
        try:
            await member.send(f"Welcome, {member.mention}!")
        except disnake.HTTPException:
            logger.warning(f"Failed to send welcome message to {member}")

    async def update_member_count(self):
        while True:
            guild = self.get_guild(123456789)  # Replace with your guild ID
            member_count_channel = guild.get_channel(987654321)  # Replace with your channel ID
            
            try:
                await member_count_channel.edit(name=f"Members: {guild.member_count}")
                logger.info(f"Updated member count to {guild.member_count}")
            except disnake.HTTPException:
                logger.warning("Failed to update member count")
            
            await asyncio.sleep(60)  # Wait for 1 minute before updating again

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
