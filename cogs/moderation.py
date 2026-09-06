import discord
from discord.ext import commands
from discord import app_commands

class Moderation(commands.Cog):
    """Server moderation commands."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Kicks a member from the server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.kick(reason=reason)
        await interaction.response.send_message(f" **{member.mention}** has been kicked. Reason: {reason}")

    @app_commands.command(name="ban", description="Bans a member from the server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        await member.ban(reason=reason)
        await interaction.response.send_message(f" **{member.mention}** has been banned. Reason: {reason}")

    @app_commands.command(name="clear", description="Deletes a specific number of messages.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("The number must be greater than 0.", ephemeral=True)
        
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f" Deleted {len(deleted)} message(s).")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
