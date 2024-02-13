import asyncio
import discord
import json
import os
from discord.ext import commands
import config

intents = discord.Intents.all()


def get_server_prefix(bot, message):
    with open("./json_files/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_server_prefix, intents=intents)


@bot.event
async def on_guild_join(guild):
    try:
        with open("./json_files/prefixes.json", "r") as f:
            prefixes = json.load(f)
    except FileNotFoundError:
        prefixes = {}

    prefixes[str(guild.id)] = "!"

    with open("./json_files/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open("./json_files/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("./json_files/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@bot.command()
@commands.has_permissions(administrator=True)
async def set_prefix(ctx, new_prefix: str):
    with open("./json_files/prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = new_prefix

    with open("./json_files/prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"Prefix changed to `{new_prefix}`")


@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    print("sync command")
    if ctx.author.id == config.MY_USER_ID:
        await bot.tree.sync()
        await ctx.send("Command tree synced.")
    else:
        await ctx.send("You must be the owner to use this command!")


@bot.event
async def on_ready():
    print("Bot connected to Discord")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(config.TOKEN)


asyncio.run(main())
