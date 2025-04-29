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
        description="Bans a member from the server.",
        options=[
            Option("member", "The member to ban.", OptionType.user, required=True),
            Option("reason", "Reason for banning.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _ban(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member,
        reason: str | None = None,
    ) -> None:
        await inter.guild.ban(member, reason=reason)
        await inter.send(f"Banned {member.mention}!")

    @commands.slash_command(
        name="softban",
        description="Softbans a member (ban & unban to delete messages).",
        options=[
            Option("member", "The member to softban.", OptionType.user, required=True),
            Option("reason", "Reason for softbanning.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _softban(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member,
        reason: str | None = None,
    ) -> None:
        await inter.guild.ban(member, reason=reason, delete_message_days=7)
        await inter.guild.unban(member)
        await inter.send(f"Softbanned {member.mention}!")

    @commands.slash_command(
        name="unban",
        description="Unbans a member from the server.",
        options=[
            Option("user_id", "The user ID of the member to unban.", OptionType.string, required=True)
        ],
        default_member_permissions=disnake.Permissions(ban_members=True),
        dm_permission=False,
    )
    async def _unban(self, inter: disnake.CommandInteraction, user_id: str) -> None:
        try:
            user = await self.bot.fetch_user(int(user_id))
            await inter.guild.unban(user)
            await inter.send(f"Unbanned {user.name}#{user.discriminator}")
        except Exception as e:
            await inter.send(f"Failed to unban: {e}", ephemeral=True)

    @commands.slash_command(
        name="kick",
        description="Kicks a member from the server.",
        options=[
            Option("member", "The member to kick.", OptionType.user, required=True),
            Option("reason", "Reason for kicking.", OptionType.string),
        ],
        default_member_permissions=disnake.Permissions(kick_members=True),
        dm_permission=False,
    )
    async def _kick(
        self,
        inter: disnake.CommandInteraction,
        member: disnake.Member,
        reason: str = "No reason provided.",
    ) -> None:
        await inter.guild.kick(member, reason=reason)
        await inter.send(f"Kicked {member.mention}!")

    @commands.slash_command(
        name="mkinvite",
        description="Generates an invite link to this server.",
        dm_permission=False,
    )
    async def _mkinvite(self, inter: disnake.CommandInteraction) -> None:
        invite = await inter.channel.create_invite(max_age=0, max_uses=0)
        await inter.send(f"Invite: https://discord.gg/{invite.code}")

    @commands.slash_command(
        name="invites",
        description="Shows all invites for the server.",
        dm_permission=False,
    )
    async def _invites(self, inter: disnake.CommandInteraction) -> None:
        invites = await inter.guild.invites()
        embed = disnake.Embed(title="Server Invites")

        if not invites:
            embed.description = "No invites found."
        else:
            for i, invite in enumerate(invites, start=1):
                link = f"https://discord.gg/{invite.code}"
                embed.add_field(
                    name=f"Invite {i}",
                    value=f"[{link}] | Uses: {invite.uses or 0} | Max Age: {invite.max_age}",
                    inline=False,
                )
        await inter.send(embed=embed)

    @commands.slash_command(
        name="pin",
        description="Pins a message by its ID.",
        options=[
            Option("id", "The ID of the message to pin.", OptionType.integer, required=True)
        ],
        default_member_permissions=disnake.Permissions(manage_messages=True),
        dm_permission=False,
    )
    async def _pin(self, inter: disnake.CommandInteraction, id: int) -> None:
        try:
            message = await inter.channel.fetch_message(id)
            await message.pin()
            await inter.send(f"Pinned message: {message.jump_url}")
        except disnake.NotFound:
            await inter.send("Message not found.", ephemeral=True)
        except Exception as e:
            await inter.send(f"Error pinning message: {e}", ephemeral=True)

    @commands.slash_command(
        name="pins",
        description="Lists pinned messages in the current channel.",
        dm_permission=False,
    )
    async def _pins(self, inter: disnake.CommandInteraction) -> None:
        messages = await inter.channel.pins()
        embed = disnake.Embed(title="Pinned Messages")

        if not messages:
            embed.description = "No pinned messages."
        else:
            for i, msg in enumerate(messages, start=1):
                preview = msg.content[:40] + ("..." if len(msg.content) > 40 else "")
                embed.add_field(name=f"{i}.", value=f"[{preview}]({msg.jump_url})", inline=False)

        await inter.send(embed=embed)

    @commands.slash_command(
        name="unpinall",
        description="Unpins all pinned messages in the current channel.",
        dm_permission=False,
    )
    async def _unpinall(self, inter: disnake.CommandInteraction) -> None:
        messages = await inter.channel.pins()
        for message in messages:
            await message.unpin()
        await inter.send(f"Unpinned {len(messages)} messages.")

    @commands.slash_command(
        name="slowmode",
        description="Set the slowmode delay in seconds.",
        options=[
            Option("seconds", "Time between messages (0 to disable).", OptionType.integer, min_value=0, max_value=21600, required=True)
        ],
        dm_permission=False,
    )
    @commands.has_permissions(manage_channels=True)
    async def _slowmode(self, inter: disnake.CommandInteraction, seconds: int) -> None:
        await inter.channel.edit(slowmode_delay=seconds)
        await inter.send(f"Slowmode set to {seconds} seconds." if seconds else "Slowmode disabled.")


def setup(bot):
    bot.add_cog(Moderation(bot))
