# cogs/music.py

"""
Music cog for commands.
"""


import asyncio
from typing import Any, Dict, Optional

import disnake
import youtube_dl
from disnake.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(disnake.PCMVolumeTransformer):
    def __init__(
        self, source: disnake.AudioSource, *, data: Dict[str, Any], volume: float = 0.5
    ):
        super().__init__(source, volume)

        self.title = data.get("title")

    @classmethod
    async def from_url(
        cls,
        url,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        stream: bool = False,
    ):
        loop = loop or asyncio.get_event_loop()
        data: Any = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)

        return cls(disnake.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="join", description="Joins a voice channel.")
    async def join(self, inter: disnake.CommandInter, *, channel: disnake.VoiceChannel):
        if inter.voice_client is not None:
            return await inter.voice_client.move_to(channel)

        await channel.connect()

    @commands.slash_command(
        name="playlocal", description="Plays a music from the local filesystem."
    )
    async def playlocal(self, inter: disnake.CommandInter, *, query: str):
        await self.ensure_voice(inter)
        source = disnake.PCMVolumeTransformer(disnake.FFmpegPCMAudio(query))
        inter.voice_client.play(
            source, after=lambda e: print(f"Player error: {e}") if e else None
        )

        await inter.send(f"Now playing: {query}")

    @commands.slash_command(
        name="playweb", description="Plays anything from a URL (e.g. YouTube)."
    )
    async def playweb(self, inter: disnake.CommandInter, *, url: str):
        await self._play_url(inter, disnake.CommandInter, url=url, stream=False)

    @commands.slash_command(
        name="stream", description="Streams media from a URL (e.g. YouTube)."
    )
    async def stream(self, inter: disnake.CommandInter, *, url: str):
        await self._play_url(inter, disnake.CommandInter, url=url, stream=True)

    async def _play_url(self, inter: disnake.CommandInter, *, url: str, stream: bool):
        await self.ensure_voice(inter)
        async with inter.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=stream)
            inter.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        await inter.send(f"Now playing: {player.title}")

    @commands.slash_command(name="volume", description="Sets the volume of the player.")
    async def volume(self, inter: disnake.CommandInter, volume: int):
        if inter.voice_client is None:
            return await inter.send("Not connected to a voice channel.")

        inter.voice_client.source.volume = volume / 100
        await inter.send(f"Changed volume to {volume}%")

    @commands.slash_command(name="stop", description="Stops the music player.")
    async def stop(self, inter):
        await inter.voice_client.disconnect()

    async def ensure_voice(self, inter):
        if inter.voice_client is None:
            if inter.author.voice:
                await inter.author.voice.channel.connect()
            else:
                await inter.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

        elif inter.voice_client.is_playing():
            inter.voice_client.stop()


def setup(bot):
    bot.add_cog(Music(bot))
