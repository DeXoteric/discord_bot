import os
import random
from discord.ext import commands


class MagicEightball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.command(aliases=["8ball", "eightball", "magicball"])
    async def magic_eightball(self, ctx, question=""):
        if question == "":
            await ctx.reply("You have to ask a question", mention_author=False)
        else:
            with open("./text_files/magic_eightball_responses.txt", "r") as f:
                random_response = random.choice(f.readlines())
            await ctx.reply(random_response, mention_author=False)


async def setup(bot):
    await bot.add_cog(MagicEightball(bot))
