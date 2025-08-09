from discord.ext import commands
from comandos import COMMANDS

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMANDS["ping"])
    async def ping(self, ctx):
        await ctx.send('Pong!')

async def setup(bot):
    await bot.add_cog(Ping(bot))
