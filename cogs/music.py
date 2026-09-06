import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp

# yt-dlp configuration options for audio extraction
YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

# FFmpeg options to stabilize the audio stream (auto-reconnect on network instability)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)


class Music(commands.Cog):
    """Voice commands and audio playback."""

    def __init__(self, bot):
        self.bot = bot

    async def ensure_voice(self, interaction: discord.Interaction) -> bool:
        """Verifies and handles connection to the user's voice channel."""
        if not interaction.user.voice:
            await interaction.response.send_message("You must be in a voice channel!", ephemeral=True)
            return False

        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await channel.connect()
        elif interaction.guild.voice_client.channel != channel:
            await interaction.guild.voice_client.move_to(channel)

        return True

    @app_commands.command(name="play", description="Plays music from a URL or YouTube search.")
    async def play(self, interaction: discord.Interaction, query: str):
        if not await self.ensure_voice(interaction):
            return

        await interaction.response.defer()

        voice_client = interaction.guild.voice_client

        try:
            player = await YTDLSource.from_url(query, loop=self.bot.loop, stream=True)
            
            if voice_client.is_playing():
                voice_client.stop()

            voice_client.play(player, after=lambda e: print(f'Playback error: {e}') if e else None)
            await interaction.followup.send(f" Now playing: **{player.title}**")

        except Exception as e:
            await interaction.followup.send(f" Unable to play track: {e}")

    @app_commands.command(name="stop", description="Stops the music and mutes playback.")
    async def stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await interaction.response.send_message(" Music stopped.")
        else:
            await interaction.response.send_message("No music is currently playing.", ephemeral=True)

    @app_commands.command(name="leave", description="Disconnects the bot from the voice channel.")
    async def leave(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await interaction.response.send_message(" Disconnected from the voice channel.")
        else:
            await interaction.response.send_message("I am not in any voice channel.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
