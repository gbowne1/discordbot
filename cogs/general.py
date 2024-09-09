# cogs/general.py

"""
General cog for commands.
"""


import disnake
from disnake import Option, OptionType
from disnake.ext import commands


class HelpView(disnake.ui.View):
    def __init__(self, *, timeout: float = 180) -> None:
        super().__init__(timeout=timeout)

        self.add_item(
            disnake.ui.Button(
                label="My Source Code",
                style=disnake.ButtonStyle.link,
                url="https://github.com/taotnpwaft/discordbot",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="The Art of Tech | GitHub",
                style=disnake.ButtonStyle.link,
                url="https://github.com/taotnpwaft",
            )
        )


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_before_slash_command_invoke(
        self, inter: disnake.CommandInter
    ) -> None:
        await inter.response.defer()

    @commands.slash_command(name="help", description="Get to know me!")
    async def _help(self, inter: disnake.CommandInter) -> None:
        embed = disnake.Embed(
            title="Hi there! This is Tao!",
            description="""
            I hang around, wander and manage this server. I\'m a general-purpose Discord bot.
            I can only do moderation stuff for now, but I think I'm growing up fast and I'll be
            able to do much more pretty soon. You can, for now, ask about me to the
            moderators of the Discord server.
            """,
        ).set_thumbnail(url=self.bot.user.avatar)
        await inter.send(embed=embed, view=HelpView())

    @commands.slash_command(
        name="greet",
        description="Greets a member.",
        options=[
            Option(
                "member",
                "The server member you wish to greet.",
                OptionType.user,
                required=True,
            )
        ],
        dm_permission=False,
    )
    async def _greet(self, inter: disnake.CommandInter, member: disnake.Member):
        await inter.send(f"Greetings, {member.mention}!")

    @commands.slash_command(
        name="serverinfo",
        description="Get information about the server.",
        dm_permission=False,
    )
    async def _serverinfo(self, inter: disnake.CommandInter):
        embed = (
            disnake.Embed(
                title="Server Information",
            )
            .add_field(name="Server Name", value=inter.guild.name, inline=True)
            .add_field(name="Server ID", value=inter.guild.id, inline=True)
            .add_field(name="Owner", value=inter.guild.owner.mention, inline=True)
            .add_field(
                name="Server Created On",
                value=inter.guild.created_at.strftime("%m/%d/%Y"),
                inline=True,
            )
            .add_field(name="Member Count", value=inter.guild.member_count, inline=True)
            .add_field(
                name="Boost Count",
                value=inter.guild.premium_subscription_count,
                inline=True,
            )
        )

        if inter.guild.icon:
            embed.set_image(url=inter.guild.icon)

        await inter.send(embed=embed)

    @commands.slash_command(
        name="ping", description="Get stats about the bot.", dm_permission=True
    )
    async def _ping(self, inter: disnake.CommandInter):
        embed = disnake.Embed(title="Pong!").add_field(
            name="Latency", value=f"{round(inter.bot.latency * 1000)}ms", inline=True
        )

        await inter.send(embed=embed)

    # show member count in VC
    @commands.slash_command(
        name="membercount",
        description="Shows the current member count in the server.",
        options=[
            Option(
                "sticky",
                "Set True to show member count in side bar.",
                OptionType.boolean,
            )
        ],
        dm_permission=False,
    )
    async def _membercount(
        self, inter: disnake.CommandInteraction, sticky: bool = False
    ) -> None:
        embed = disnake.Embed(
            title="Member Count",
            description=f"There are {inter.guild.member_count} members in this server.",
        )

        for channel in inter.guild.channels:
            if channel.name.startswith("Members:"):
                await channel.delete()

        if sticky:
            await inter.guild.create_voice_channel(
                name=f"Members: {inter.guild.member_count}",
                position=0,
                overwrites={
                    inter.guild.default_role: disnake.PermissionOverwrite(
                        connect=False
                    ),
                    inter.guild.me: disnake.PermissionOverwrite(
                        manage_channels=True, connect=False
                    ),
                },
            )
            embed.set_footer(text="Sticky mode enabled.")
            await inter.send(embed=embed)

        else:
            await inter.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
