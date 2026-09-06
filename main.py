import os
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(level=logging.INFO)

# Intent configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- COGS CONFIGURATION ---
# Comment or delete a line to disable a module
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
        print(f" Synchronized {len(synced)} slash command(s).")
    except Exception as e:
        print(f" Synchronization error: {e}")

async def load_extensions():
    for ext in ENABLED_EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f" Loaded cog: {ext}")
        except Exception as e:
            print(f" Error loading {ext}: {e}")

async def main():
    if not TOKEN:
        raise ValueError(" Discord token not found. Make sure you have configured DISCORD_TOKEN in your .env file")

    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
