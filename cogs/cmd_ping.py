import os
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.command()
    async def ping(self, ctx):
        bot_latency = round(self.bot.latency * 1000)
        await ctx.reply(f"Bot latency: {bot_latency} ms.", mention_author=False)


async def setup(bot):
    await bot.add_cog(Ping(bot))
