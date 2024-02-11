import discord
import os
from discord.ext import commands
import config


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.logs_channel = self.bot.get_channel(config.SERVER_LOGS_CHANNEL_ID)
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: str = None):
        if amount is None:
            await ctx.channel.purge(limit=1)
            return
        try:
            amount = int(amount)
        except ValueError:
            await self.invalid_syntax(ctx)
            return

        if amount < 1:
            await self.invalid_syntax(ctx)
            return

        await ctx.channel.purge(limit=amount)

    async def invalid_syntax(self, ctx):
        await ctx.reply(
            "Please specify a valid positive number.\nExample: `!clear 6`",
            mention_author=False,
        )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(member, reason=reason)

        confirmation_embed = discord.Embed(title="Kick", color=discord.Color.blue())
        confirmation_embed.set_thumbnail(url=ctx.author.avatar)
        confirmation_embed.add_field(
            name="Moderator:", value=ctx.author.display_name, inline=False
        )
        confirmation_embed.add_field(name="Username:", value=member.name, inline=False)
        confirmation_embed.add_field(
            name="Display name:", value=member.display_name, inline=False
        )
        confirmation_embed.add_field(name="Reason:", value=reason, inline=False)

        await self.logs_channel.send(embed=confirmation_embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(member, reason=reason)

        confirmation_embed = discord.Embed(title="Ban", color=discord.Color.red())
        confirmation_embed.set_thumbnail(url=ctx.author.avatar)
        confirmation_embed.add_field(
            name="Moderator:", value=ctx.author.display_name, inline=False
        )
        confirmation_embed.add_field(name="Username:", value=member.name, inline=False)
        confirmation_embed.add_field(
            name="Display name:", value=member.display_name, inline=False
        )
        confirmation_embed.add_field(name="User ID:", value=member.id, inline=False)
        confirmation_embed.add_field(name="Reason:", value=reason, inline=False)

        await self.logs_channel.send(embed=confirmation_embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userID, *, reason=None):
        user = await self.bot.fetch_user(userID)
        await ctx.guild.unban(user)

        confirmation_embed = discord.Embed(title="Unban", color=discord.Color.green())
        confirmation_embed.set_thumbnail(url=ctx.author.avatar)
        confirmation_embed.add_field(
            name="Moderator:", value=ctx.author.display_name, inline=False
        )
        confirmation_embed.add_field(name="Username:", value=user.name, inline=False)
        confirmation_embed.add_field(
            name="Display name:", value=user.display_name, inline=False
        )
        confirmation_embed.add_field(name="User ID:", value=userID, inline=False)
        confirmation_embed.add_field(name="Reason:", value=reason, inline=False)

        await self.logs_channel.send(embed=confirmation_embed)

    @commands.command()
    async def test(self, ctx):
        await self.logs_channel.send("test")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
