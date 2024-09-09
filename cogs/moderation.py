# cogs/moderation.py

"""
Moderation cog for commands.
"""


import disnake
from disnake import Option, OptionType
from disnake.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        name="ban",
        description="Bans people.",
        options=[
            Option(
                "member",
                "The server member you want to ban.",
                OptionType.user,
                required=True,
            ),
            Option("reason", "Reason for banning the person.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _ban(
        self,
        inter: disnake.CommandInter,
        member: disnake.Member,
        reason: str | None = None,
    ) -> None:
        await inter.guild.ban(member, reason=reason)
        await inter.send(f"Banned {member.name}{member.discriminator}!")

    @commands.slash_command(
        name="sofban",
        description="Softans people to wipe their messages.",
        options=[
            Option(
                "member",
                "The server member you want to ban.",
                OptionType.user,
                required=True,
            ),
            Option("reason", "Reason for softbanning the person.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _softban(
        self,
        inter: disnake.CommandInter,
        member: disnake.Member,
        reason: str | None = None,
    ) -> None:
        await inter.guild.ban(member, reason=reason, delete_message_days=7)
        await inter.send(f"Softbanned {member.name}{member.discriminator}!")

    @commands.slash_command(
        name="unban",
        description="Unbans a member from the server.",
        options=[
            Option(
                "member",
                "The server member you'd like to unban.",
                OptionType.user,
                required=True,
            )
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _unban(self, inter: disnake.CommandInter, member: disnake.Member) -> None:
        await inter.guild.unban(member)
        await inter.send(f"Unbanned {member.display_name}!")

    @commands.slash_command(
        name="kick",
        description="Kicks a member from the server.",
        options=[
            Option(
                "member",
                "The server member you'd like to kick.",
                OptionType.user,
                required=True,
            ),
            Option("reason", "Reason for kicking the person.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(kick_members=True),
        dm_permission=False,
    )
    async def _kick(
        self,
        inter: disnake.CommandInter,
        member: disnake.Member,
        reason: str = "No reason provided.",
    ) -> None:
        await inter.guild.kick(member, reason=reason)
        await inter.send(f"Kicked {member.name}{member.discriminator}!")

    @commands.slash_command(
        name="mkinvite",
        description="Get an invite link to this server.",
        dm_permission=False,
    )
    async def _mkinvite(self, inter: disnake.CommandInter) -> None:
        invite = await inter.channel.create_invite(max_age=0, max_uses=0)
        await inter.send(
            f"Here's an invite link to this server: https://discord.gg/{invite.code}"
        )

    @commands.slash_command(
        name="invites",
        description="List all invites for this server.",
        dm_permission=False,
    )
    async def _invites(self, inter: disnake.CommandInter) -> None:
        invites = await inter.guild.invites()
        embed = disnake.Embed(title="Invites")
        if invites:
            count = 1
            for invite in invites:
                link = f"https://discord.gg/{invite.code}"
                embed.add_field(
                    name=f"`{count}: {invite.code}`",
                    value=f"Uses: {invite.uses} | Max Age: {invite.max_age} | [Link]({link})",
                    inline=False,
                )
                count += 1
        else:
            embed.description = "No invites found."
        await inter.send(embed=embed)

    @commands.slash_command(
        name="pin",
        description="Pins a message",
        options=[
            Option("id", "The ID of the message.", OptionType.integer, required=True)
        ],
        default_member_permissions=disnake.Permissions(manage_messages=True),
        dm_permission=False,
    )
    async def _pin(self, inter: disnake.CommandInter, id: int) -> None:
        message = self.bot.get_message(id)

        await message.pin()
        await inter.send(f"Pinned message: {message.jump_url}")

    @commands.slash_command(
        name="pins",
        description="Shows the pinned messages in current channel.",
        dm_permission=False,
    )
    async def _pins(self, inter: disnake.CommandInter) -> None:
        embed = disnake.Embed(title="Pinned Messages")
        message: disnake.Message

        for count, message in enumerate(inter.channel.pins):
            embed.add_field(
                name=f"#{count} - {message.content[:15]}...",
                value=f"[Jump to message]({message.jump_url})",
                inline=False,
            )

        await inter.send(embed=embed)

    @commands.slash_command(
        name="unpinall",
        description="Unpins all pinned messages in current channel.",
        dm_permission=False,
    )
    async def _unpinall(self, inter: disnake.CommandInter) -> None:
        message: disnake.Message

        for message in enumerate(inter.channel.pins):
            await message.unpin()

        await inter.send(f"Unpinned {len(inter.channel.pins)} messages.")

    # slowmode
    @commands.slash_command(
        name='slowmode',
        description='Sets slowmode for the current channel.',
        options=[
            Option(
                'seconds',
                'The amount of seconds to set the slowmode to. Set 0 to disable.',
                OptionType.integer,
                min_value=0,
                max_value=21600,
                required=True,
            )
        ],
        dm_permission=False,
    )
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, inter: disnake.CommandInter, seconds: int) -> None:
        await inter.channel.edit(slowmode_delay=seconds)
        message = f'Slowmode set to {seconds} seconds.' if seconds else 'Slowmode disabled.'
        await inter.send(message)


def setup(bot):
    bot.add_cog(Moderation(bot))
