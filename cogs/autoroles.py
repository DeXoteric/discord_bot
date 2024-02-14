import os
from discord.ext import commands
import config


class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != config.WELCOME_CHANNEL_ID:
            return
        if payload.emoji.name == "✅":
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(config.MEMBER_ROLE_ID)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id != config.WELCOME_CHANNEL_ID:
            return
        if payload.emoji.name == "✅":
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(config.MEMBER_ROLE_ID)
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(Autoroles(bot))
