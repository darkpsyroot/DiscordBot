from discord.ext.commands import Group

class CommandsService:
    def __init__(self, bot):
        self.bot = bot

    async def obtener_lista_comandos(self, ctx, allowed_roles=None):
        """
        Devuelve la lista de comandos propios del bot filtrando por roles.
        allowed_roles: lista de roles del usuario para filtrar comandos protegidos.
        """
        texto = ""

        # Primero detectamos automáticamente los cogs propios
        mis_cogs = set()
        for cmd in self.bot.commands:
            if cmd.cog_name:  # si tiene cog
                # Podemos asumir que todos tus cogs están dentro de cogs.*, o que no son cogs de discord.py
                mis_cogs.add(cmd.cog_name)

        def listar_comandos(cmds, nivel=0):
            salida = ""
            indent = "    " * nivel
            for cmd in cmds:
                # Filtrar por cogs propios
                if not cmd.cog_name or cmd.cog_name not in mis_cogs:
                    continue

                # Filtrar mavuika/zhongli si no tiene rol
                if cmd.name in ("mavuika", "zhongli"):
                    if not allowed_roles or not any(r in ["Arconte", "ZhongliSimp"] for r in allowed_roles):
                        continue

                salida += f"{indent}• `{ctx.prefix}{cmd.name}`\n"

                # Recursivo para subcomandos
                if isinstance(cmd, Group):
                    salida += listar_comandos(cmd.commands, nivel + 1)
            return salida

        texto = listar_comandos(self.bot.commands)
        return "📋 **Lista de comandos y subcomandos disponibles:**\n" + texto
