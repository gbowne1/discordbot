import os
import logging
import asyncio
from typing import Optional
import disnake
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Secrets:
    @staticmethod
    def get_token() -> Optional[str]:
        return os.getenv("DISCORD_TOKEN")

    @classmethod
    def check_env(cls) -> bool:
        token = cls.get_token()
        if not token:
            logger.error("DISCORD_TOKEN is not set in environment variables.")
            return False
        return True


class DiscordBot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)
        self.bg_task = None

    async def on_ready(self):
        logger.info(f"{self.user} has connected to Discord!")
        self.bg_task = self.loop.create_task(self.update_member_count())

    async def on_member_join(self, member: disnake.Member):
        logger.info(f"{member} has joined the server.")

    async def update_member_count(self):
        await self.wait_until_ready()
        guild = self.get_guild(123456789)  # Replace with your actual guild ID
        member_count_channel = guild.get_channel(987654321)  # Replace with your actual channel ID

        while not self.is_closed():
            try:
                await member_count_channel.edit(name=f"Members: {guild.member_count}")
                logger.info(f"Updated member count to {guild.member_count}")
            except disnake.HTTPException as e:
                logger.warning(f"Failed to update member count: {e}")
            await asyncio.sleep(60)


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
        logger.error("Missing configuration. Exiting.")
        return

    bot = DiscordBot()
    load_extensions(bot)

    try:
        await bot.start(Secrets.get_token())
    except disnake.LoginFailure:
        logger.error("Invalid DISCORD_TOKEN.")
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
