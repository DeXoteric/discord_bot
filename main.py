import discord
from discord.ext import commands

import const

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print("Bot connected to Discord")


client.run(const.TOKEN)
