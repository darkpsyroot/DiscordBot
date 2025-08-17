from discord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send("Escribe `!furina lista comandos` para ver los comandos disponibles.")

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
