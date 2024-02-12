import discord
import os
import random
import sqlite3
from discord.ext import commands
from discord import app_commands


class InvestmentGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = self.db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                guild_id TEXT,
                user_id TEXT,
                balance INTEGER DEFAULT 0,
                prestige INTEGER DEFAULT 0,
                PRIMARY KEY (guild_id, user_id)
            )
            """
        )
        self.db.commit()
        self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    @app_commands.command(name="join", description="Join the investment game")
    async def join_game(self, interaction: discord.Interaction):
        db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = db.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (guild_id, user_id, balance, prestige) VALUES (?, ?, ?, ?)",
                (interaction.guild.id, interaction.user.id, 1000, 0),
            )
            db.commit()
            await interaction.response.send_message(
                "You successfully joined the game and received 1000 coins!"
            )
        except sqlite3.IntegrityError:
            await interaction.response.send_message(
                "You are already a part of the investment game."
            )
        finally:
            db.close()

    @app_commands.command(name="balance")
    async def balance(self, interaction: discord.Interaction):
        db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = db.cursor()
        data = cursor.execute(
            "SELECT balance FROM users WHERE guild_id = ? AND user_id = ?",
            (
                interaction.guild.id,
                interaction.user.id,
            ),
        )
        balance = data.fetchone()
        db.commit()
        db.close()
        await interaction.response.send_message(
            f"Your current balance is {balance[0]} coins!"
        )

    @app_commands.command(name="invest")
    async def invest(self, interaction: discord.Interaction, amount: int):
        pass


async def setup(bot):
    await bot.add_cog(InvestmentGame(bot))
