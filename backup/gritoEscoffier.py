"""
antes estaba en cogs/extras/
"""

from discord.ext import commands
import discord
from comandos import COMMANDS

class GritoEscoffier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMANDS["grito_escoffier"])
    async def grito_escoffier(self, ctx):
        imagen_path = "assets/imagenes/gritoEscoffier.jpeg"
        audio_path = "assets/audio/gritoescoffier.mp3"

        await ctx.send(
            content="¡Grito de Escoffier!",
            files=[
                discord.File(imagen_path),
                discord.File(audio_path)
            ]
        )

async def setup(bot):
    await bot.add_cog(GritoEscoffier(bot))
