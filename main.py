import os
import asyncio
import logging
import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)

# Intents Configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- COGS CONFIGURATION ---
# Comment out or remove a line to disable a module
ENABLED_EXTENSIONS = [
    "cogs.moderation",
    "cogs.utility",
    "cogs.fun",
    "cogs.music",
]

@bot.event
async def on_ready():
    print(f" Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f" Synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Sync error: {e}")

async def load_extensions():
    for ext in ENABLED_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f" Loaded cog: {ext}")
        except Exception as e:
            print(f" Error loading {ext}: {e}")

async def main():
    async with bot:
        await load_extensions()

        await bot.start("DISCORD_TOKEN")

if __name__ == "__main__":
    asyncio.run(main())
