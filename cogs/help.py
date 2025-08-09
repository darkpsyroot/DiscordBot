from discord.ext import commands

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx):
        await ctx.send("Escribe `!comandos listacomandos` para ver los comandos disponibles.")

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
