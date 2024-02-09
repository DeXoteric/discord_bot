import os
import random
from discord.ext import commands


class RollDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.command(aliases=["roll", "dice"])
    async def roll_dice(self, ctx, dice_sides: str = None):
        if dice_sides is None:
            await self.invalid_syntax(ctx)
            return
        try:
            dice_sides = int(dice_sides)
        except ValueError:
            await self.invalid_syntax(ctx)
            return

        if dice_sides <= 0:
            await self.invalid_syntax(ctx)
            return

        result = random.randint(1, dice_sides)
        await ctx.reply(
            f"You rolled a d{dice_sides} and got: {result}", mention_author=False
        )

    async def invalid_syntax(self, ctx):
        await ctx.reply(
            "Please specify a valid positive number of sides.\nExample: `!dice 6` or `!roll 6`",
            mention_author=False,
        )


async def setup(bot):
    await bot.add_cog(RollDice(bot))
