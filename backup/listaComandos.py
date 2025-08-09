from discord.ext import commands
import discord

class ListaComandos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="comandos")
    async def mostrar_comandos(self, ctx):
        comandos = self.bot.commands
        lista = [f"• `{ctx.prefix}{comando.name}`" for comando in comandos if not comando.hidden]
        texto = "\n".join(lista)

        await ctx.send(
            content="📋 **Lista de comandos disponibles:**\n" + texto
        )

async def setup(bot):
    await bot.add_cog(ListaComandos(bot))
