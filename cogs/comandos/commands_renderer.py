from discord.ext import commands

class CommandsRenderer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def render_for_user(self, user, cog_name, prefix="!"):
        roles = [r.name for r in user.roles]
        texto = "📋 **Lista de comandos y subcomandos disponibles:**\n"

        cog = self.bot.get_cog(cog_name.capitalize())
        if not cog:
            return "❌ Cog no encontrado."

        texto += f"• `{prefix}{cog_name}`\n"

        # Subcomandos de Furina con filtro de roles
        if cog_name == "furina" and hasattr(cog, "subcommands_service"):
            for sub_name in cog.subcommands_service.subcommands.keys():
                # Comandos sensibles que requieren rol Arconte/Zhongli
                if sub_name in ["stop", "ping", "permisos", "expulsar", "banear"]:
                    if not any(r in roles for r in ["Arconte", "ZhongliSimp"]):
                        continue
                texto += f"    • `{prefix}furina {sub_name}`\n"

        # Para Mavuika y Zhongli: listar todos los comandos del cog
        else:
            for command in cog.get_commands():
                texto += f"    • `{prefix}{command.name}`\n"

        return texto

async def setup(bot):
    await bot.add_cog(CommandsRenderer(bot))
