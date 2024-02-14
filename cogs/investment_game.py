import discord
import math
import os
import random
import sqlite3
from discord.ext import commands
from discord import app_commands

STARTING_BALANCE = 1000.0
FIRST_PRESTIGE_LEVEL_AT = 10000.0
INVEST_COOLDOWN = 1.0
PRESTIGE_MULTIPLIER = 1.05


class InvestmentGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = self.db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT NOT NULL,
                guild_id TEXT NOT NULL,
                balance REAL NOT NULL,
                prestige INTEGER NOT NULL,
                next_prestige_level REAL NOT NULL,
                total_earned REAL NOT NULL,
                bankruptcies INTEGER NOT NULL,
                successful_investments INTEGER NOT NULL,
                failed_investments INTEGER NOT NULL,
                PRIMARY KEY (user_id, guild_id)
            )
            """
        )
        self.db.commit()
        self.db.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready!")

    group = app_commands.Group(name="ig", description="Investment Game Commands")

    @group.command(name="join", description="Join the investment game")
    async def join_game(self, interaction: discord.Interaction):
        db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = db.cursor()
        try:
            cursor.execute(
                """INSERT INTO users 
                (user_id, guild_id, balance, prestige, next_prestige_level, total_earned, bankruptcies, successful_investments, failed_investments) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    interaction.user.id,
                    interaction.guild.id,
                    STARTING_BALANCE,
                    0,
                    FIRST_PRESTIGE_LEVEL_AT,
                    0,
                    0,
                    0,
                    0,
                ),
            )
            db.commit()
            await interaction.response.send_message(
                f"You successfully joined the game and received {STARTING_BALANCE} coins!"
            )
        except sqlite3.IntegrityError:
            await interaction.response.send_message(
                "You are already a part of the investment game."
            )
        finally:
            db.close()

    @group.command(name="stats", description="View your stats or someone else's")
    @app_commands.checks.cooldown(1, 5, key=lambda i: (i.guild_id, i.user.id))
    async def stats(
        self, interaction: discord.Interaction, member: discord.Member = None
    ):
        if member is None:
            member = interaction.user

        db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = db.cursor()
        cursor.execute(
            """SELECT balance, prestige, next_prestige_level, total_earned, bankruptcies, successful_investments, failed_investments 
            FROM users WHERE guild_id = ? AND user_id = ?""",
            (
                interaction.guild.id,
                member.id,
            ),
        )
        data = cursor.fetchone()
        db.commit()
        db.close()

        if data is None:
            await interaction.response.send_message(
                f"{member.display_name} is not a part of the investment game."
            )
            return

        (
            balance,
            prestige,
            next_prestige_level,
            total_earned,
            bankruptcies,
            successful_investments,
            failed_investments,
        ) = data

        if successful_investments == 0 or failed_investments == 0:
            success_rate = 0
        else:
            success_rate = (
                successful_investments / (successful_investments + failed_investments)
            ) * 100

        embed = discord.Embed(
            title=f"Stats for {member.display_name}", color=discord.Color.random()
        )
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Balance", value=f"{balance:,} coins", inline=False)
        embed.add_field(name="Prestige level", value=f"{prestige}", inline=False)
        embed.add_field(
            name="Next prestige level at",
            value=f"{next_prestige_level:,} coins",
            inline=False,
        )
        embed.add_field(
            name="Total coins earned",
            value=f"{total_earned:,} coins",
            inline=False,
        )
        embed.add_field(
            name="Bankruptcies",
            value=f"{bankruptcies:,}",
            inline=False,
        )
        embed.add_field(
            name="Total investments",
            value=f"{successful_investments + failed_investments}",
            inline=False,
        )
        embed.add_field(
            name="Success rate",
            value=f"{success_rate:,.2f}%",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @group.command(
        name="invest",
        description=f"Invest x amount of coins for a chance to get more coins. Cooldown: {INVEST_COOLDOWN} seconds",
    )
    @app_commands.checks.cooldown(
        1, INVEST_COOLDOWN, key=lambda i: (i.guild_id, i.user.id)
    )
    async def invest(self, interaction: discord.Interaction, amount: float):
        db = sqlite3.connect("./sqlite3_files/investment_game.db")
        cursor = db.cursor()
        cursor.execute(
            "SELECT balance, prestige, next_prestige_level, total_earned, bankruptcies, successful_investments, failed_investments FROM users WHERE guild_id = ? AND user_id = ?",
            (
                interaction.guild.id,
                interaction.user.id,
            ),
        )
        (
            balance,
            prestige,
            next_prestige_level,
            total_earned,
            bankruptcies,
            successful_investments,
            failed_investments,
        ) = cursor.fetchone()

        if amount > balance:
            await interaction.response.send_message(
                "You don't have that much coins to invest."
            )
            return

        user_chance = random.randint(0, 10000) / 100
        if user_chance > 25:
            user_chance -= 25
        chance_of_success = random.randint(100, 10000) / 100
        profit_percentage = self.get_profit_percentage()

        if user_chance < chance_of_success:
            balance += amount * profit_percentage / 100
            total_earned += amount * profit_percentage / 100
            successful_investments += 1

            if balance >= next_prestige_level:
                bonus_coins = balance - next_prestige_level
                old_balance = balance
                balance = STARTING_BALANCE + bonus_coins
                prestige += 1
                next_prestige_level = self.calculate_next_prestige_level(prestige)

                await interaction.response.send_message(
                    f"You successfully invested {amount:,} coins and earned {amount * profit_percentage / 100:,.2f} coins!\n"
                    f"Your chance of success was {chance_of_success}% and your profit percentage was {profit_percentage}%.\n"
                    f"You have reached the next prestige level! Your next prestige level is at {next_prestige_level:,} coins.\n"
                    f"Your balance was {old_balance:,.2f} coins.\n"
                    f"Your balance was reset to {STARTING_BALANCE:,} coins and you received {bonus_coins:,.2f} coins extra."
                )
            else:
                await interaction.response.send_message(
                    f"You successfully invested {amount:,} coins and earned {amount * profit_percentage / 100:,.2f} coins!\n"
                    f"Your chance of success was {chance_of_success}% and your profit percentage was {profit_percentage}%.\n"
                    f"Your balance is now {balance:,.2f} coins."
                )
        else:
            balance -= amount
            failed_investments += 1

            if balance < 1:
                if prestige > 0:
                    prestige -= 1
                bankruptcies += 1
                next_prestige_level = self.calculate_next_prestige_level(prestige)
                balance = STARTING_BALANCE

                await interaction.response.send_message(
                    f"Your investment failed. You lost {amount:,} coins.\n"
                    f"Your chance of success was {chance_of_success}% and your profit percentage was {profit_percentage}%.\n"
                    f"You have run out of coins! You lost 1 prestige level (if you had any) and your balance was reset to {STARTING_BALANCE:,} coins."
                )
            else:
                await interaction.response.send_message(
                    f"Your investment failed. You lost {amount:,} coins.\n"
                    f"Your chance of success was {chance_of_success}% and your profit percentage was {profit_percentage}%.\n"
                    f"Your balance is now {balance:,.2f} coins."
                )

        cursor.execute(
            """UPDATE users 
            SET balance = ?, prestige = ?, next_prestige_level = ?, total_earned = ?, bankruptcies = ?, successful_investments = ?, failed_investments = ? 
            WHERE guild_id = ? AND user_id = ?""",
            (
                round(balance, 2),
                prestige,
                round(next_prestige_level, 2),
                round(total_earned, 2),
                bankruptcies,
                successful_investments,
                failed_investments,
                interaction.guild.id,
                interaction.user.id,
            ),
        )
        db.commit()
        db.close()

    @invest.error
    async def on_test_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)

    # Helper functions
    def calculate_next_prestige_level(self, prestige):
        return FIRST_PRESTIGE_LEVEL_AT * math.pow(PRESTIGE_MULTIPLIER, prestige)

    def get_profit_percentage(self):
        chance_for_better_profit = random.randint(0, 10000) / 100
        if chance_for_better_profit >= 99:
            return random.randint(25000, 50000) / 100
        elif chance_for_better_profit >= 95:
            return random.randint(12500, 25000) / 100
        elif chance_for_better_profit >= 85:
            return random.randint(10000, 20000) / 100
        elif chance_for_better_profit >= 60:
            return random.randint(7500, 15000) / 100
        elif chance_for_better_profit >= 30:
            return random.randint(5000, 12500) / 100
        else:
            return random.randint(2500, 10000) / 100


async def setup(bot):
    await bot.add_cog(InvestmentGame(bot))
