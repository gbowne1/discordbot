# cogs/errorhandler.py

"""
The error handler for commands.
"""


from typing import Any

import disnake
from disnake.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(
        self, inter: disnake.CommandInter, error: Any
    ) -> None:
        error = getattr(error, "original", error)
        await inter.send(error, ephemeral=True)

    @commands.Cog.listener()
    async def on_user_command_error(
        self, inter: disnake.CommandInter, error: Any
    ) -> None:
        error = getattr(error, "original", error)
        await inter.send(error, ephemeral=True)

    @commands.Cog.listener()
    async def on_message_command_error(
        self, inter: disnake.CommandInter, error: Any
    ) -> None:
        error = getattr(error, "original", error)
        await inter.send(error, ephemeral=True)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
