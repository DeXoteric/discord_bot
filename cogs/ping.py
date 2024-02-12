import discord
import os
from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @app_commands.command(name="ping", description="Get the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(
            content=f"Bot latency: {bot_latency} ms."
        )


async def setup(bot):
    await bot.add_cog(Ping(bot))
