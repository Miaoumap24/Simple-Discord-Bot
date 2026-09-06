# Copyright (C) 2026 Lixiod Technologies

import random
import discord
from discord.ext import commands
from discord import app_commands

class Fun(commands.Cog):
    """Fun and entertainment commands."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roll", description="Rolls dice (e.g., 1d6, 2d20).")
    async def roll(self, interaction: discord.Interaction, dice: str = "1d6"):
        try:
            rolls, limit = map(int, dice.lower().split('d'))
        except Exception:
            return await interaction.response.send_message("Invalid format. Use the `NdX` format (e.g., 2d6).", ephemeral=True)

        if rolls > 10 or limit > 100:
            return await interaction.response.send_message("Maximum 10 dice and 100 sides!", ephemeral=True)

        results = [random.randint(1, limit) for _ in range(rolls)]
        total = sum(results)
        await interaction.response.send_message(f" **Result:** {results} (Total: **{total}**)")

    @app_commands.command(name="8ball", description="Ask the magic 8-ball a question.")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        responses = [
            "It is certain.", "Most likely.", "Without a doubt.",
            "Ask again later.", "Cannot predict now.",
            "Don't count on it.", "My reply is no.", "Very doubtful."
        ]
        choice = random.choice(responses)
        await interaction.response.send_message(f" **Question:** {question}\n **8-Ball:** {choice}")

async def setup(bot):
    await bot.add_cog(Fun(bot))
