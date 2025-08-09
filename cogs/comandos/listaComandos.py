from discord.ext import commands
from services.commands_service import CommandsService

class ListaComandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.commands_service = CommandsService(bot)

    @commands.group(name="comandos", invoke_without_command=True)
    async def comandos(self, ctx):
        await ctx.send("Usa un subcomando, por ejemplo: !comandos listacomandos")

    @comandos.command(name="listacomandos")
    async def listacomandos(self, ctx):
        texto = await self.commands_service.obtener_lista_comandos(ctx)
        await ctx.send(content=texto)

async def setup(bot):
    await bot.add_cog(ListaComandos(bot))
