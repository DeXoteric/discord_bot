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


async def setup(bot):
    await bot.add_cog(Moderation(bot))
