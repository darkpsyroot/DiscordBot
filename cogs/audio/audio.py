from discord.ext import commands
import discord
from services.audio_service import AudioService
from comandos import COMMANDS

class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_service = AudioService()

    @commands.group(name="audio", invoke_without_command=True)
    async def audio(self, ctx):
        await ctx.send("Usa un subcomando, por ejemplo !audio grito")

    @audio.command(name=COMMANDS["grito1"])
    async def grito1(self, ctx):
        audio_path = "assets/audio/gritoescoffier.mp3"
        await self.audio_service.enviar_audio(ctx, audio_path)

    @audio.command(name=COMMANDS["grito2"])
    async def grito2(self, ctx):
        audio_path = "assets/audio/navia_fire.mp3"
        await self.audio_service.enviar_audio(ctx, audio_path)

async def setup(bot):
    await bot.add_cog(Audio(bot))
