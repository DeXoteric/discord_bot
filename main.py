import random
import discord
from discord.ext import commands, tasks
import const

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@tasks.loop(seconds=60)
async def change_status():
    with open("./text_files/bot_activity_status_list.txt", "r") as f:
        random_bot_status = random.choice(f.readlines())
    await bot.change_presence(activity=discord.CustomActivity(random_bot_status))


@bot.event
async def on_ready():
    print("Bot connected to Discord")
    change_status.start()


@bot.command()
async def ping(ctx):
    bot_latency = round(bot.latency * 1000)
    await ctx.reply(f"Bot latency: {bot_latency} ms.", mention_author=False)


@bot.command(aliases=["8ball", "eightball", "magicball"])
async def magic_eightball(ctx, question=""):
    if question == "":
        await ctx.reply("You have to ask a question", mention_author=False)
    else:
        with open("./text_files/magic_eightball_responses.txt", "r") as f:
            random_response = random.choice(f.readlines())
        await ctx.reply(random_response, mention_author=False)


bot.run(const.TOKEN)
