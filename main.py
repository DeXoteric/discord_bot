import random

import discord
from discord.ext import commands

import const

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Bot connected to Discord")


@bot.command()
async def ping(ctx):
    bot_latency = round(bot.latency * 1000)
    await ctx.reply(f"Bot latency: {bot_latency} ms.", mention_author=False)


@bot.command(aliases=["8ball", "eightball", "magicball"])
async def magic_eightball(ctx, question=""):
    if question == "":
        await ctx.reply("You have to ask a question", mention_author=False)
    else:
        with open("magic_eightball_responses.txt", "r") as f:
            responses = f.readlines()
            random_response = random.choice(responses)
        await ctx.reply(random_response, mention_author=False)


bot.run(const.TOKEN)
