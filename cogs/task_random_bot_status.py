import discord
import os
import random
from discord.ext import commands, tasks


class RandomBotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_status.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @tasks.loop(seconds=60)
    async def change_status(self):
        with open("./text_files/bot_activity_status_list.txt", "r") as f:
            random_bot_status = random.choice(f.readlines())
        await self.bot.change_presence(
            activity=discord.CustomActivity(random_bot_status)
        )


async def setup(bot):
    await bot.add_cog(RandomBotStatus(bot))
