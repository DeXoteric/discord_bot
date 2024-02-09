import discord
import os
from discord.ext import commands


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @commands.command()
    async def embed(self, ctx):
        embed_message = discord.Embed(
            title="Title of embed",
            description="Description of embed",
            color=discord.Color.random(),
        )

        embed_message.set_author(
            name=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar
        )
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(name="Field name", value="Field value", inline=False)
        embed_message.set_footer(text="This is a footer", icon_url=ctx.author.avatar)

        await ctx.send(embed=embed_message)


async def setup(bot):
    await bot.add_cog(Embed(bot))
