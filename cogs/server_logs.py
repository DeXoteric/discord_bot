import os
from discord.ext import commands
import config


class ServerLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(config.MEMBERSHIP_LOGS_CHANNEL_ID)
        await channel.send(
            f"{member.mention} (username: `{member.name}`) joined the server!"
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(config.MEMBERSHIP_LOGS_CHANNEL_ID)
        await channel.send(
            f"{member.mention} (username: `{member.name}`) left the server!"
        )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        channel = self.bot.get_channel(config.BAN_LOGS_CHANNEL_ID)
        await channel.send(
            f"{member.mention} (username: `{member.name}`) was banned from the server!"
        )

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        channel = self.bot.get_channel(config.BAN_LOGS_CHANNEL_ID)
        await channel.send(
            f"{member.mention} (username: `{member.name}`) was unbanned from the server!"
        )


async def setup(bot):
    await bot.add_cog(ServerLogs(bot))
