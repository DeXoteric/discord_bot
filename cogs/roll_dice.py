import discord
import os
import random
from discord.ext import commands
from discord import app_commands


class RollDice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @app_commands.command(
        name="dice", description="Roll a dice with a specified number of sides"
    )
    @app_commands.describe(
        dice_sides="Enter the number of sides for the dice to roll (e.g., 6 for a standard dice)"
    )
    @app_commands.rename(dice_sides="num")
    async def roll_dice(self, interaction: discord.Interaction, dice_sides: int):
        if dice_sides <= 0:
            await self.invalid_syntax(interaction)
            return

        result = random.randint(1, dice_sides)
        await interaction.response.send_message(
            content=f"You rolled a d{dice_sides} and got: {result}"
        )

    async def invalid_syntax(self, interaction):
        await interaction.response.send_message(
            content="Please specify a valid positive number of sides.\nExample: `/dice 6`"
        )


async def setup(bot):
    await bot.add_cog(RollDice(bot))
