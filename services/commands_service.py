from discord.ext.commands import Group

class CommandsService:
    def __init__(self, bot):
        self.bot = bot

    async def obtener_lista_comandos(self, ctx):
        def listar_comandos(cmds, nivel=0):
            texto = ""
            indent = "    " * nivel
            for cmd in cmds:
                texto += f"{indent}• `{ctx.prefix}{cmd.name}`\n"
                if isinstance(cmd, Group):
                    texto += listar_comandos(cmd.commands, nivel + 1)
            return texto

        texto = listar_comandos(self.bot.commands)
        return "📋 **Lista de comandos y subcomandos disponibles:**\n" + texto
