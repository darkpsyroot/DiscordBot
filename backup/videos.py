from discord.ext import commands
import discord
from comandos import COMMANDS

class Videos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMANDS["best_team"])
    async def best_team(self, ctx):
        video_path = "assets/video/BestTeam.mp4"
        await ctx.send(
            #content="🎥 ¡Mira este video del mejor equipo!",
            file=discord.File(video_path)
        )

async def setup(bot):
    await bot.add_cog(Videos(bot))
