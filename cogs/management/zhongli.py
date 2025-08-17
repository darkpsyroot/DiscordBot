import discord
from discord.ext import commands
from .permisos_handler import PermisosHandler
from services.subcommands_service import SubcommandsService
from services.openai_service import OpenAIService  # Importamos para pasar al servicio

class Zhongli(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = {"Arconte", "ZhongliSimp"}
        self.permisos_handler = PermisosHandler(bot)
        self.openai_service = OpenAIService()  # se puede compartir o usar None si no aplica
        self.subcommands_service = SubcommandsService(self, self.openai_service)

    def has_permission(self, member):
        return any(role.name in self.allowed_roles for role in member.roles)

    def is_zhongli_enabled(self):
        mavuika = self.bot.get_cog("Mavuika")
        return mavuika.zhongli_enabled if mavuika else True

    @commands.command(name="zhongli")
    async def zhongli_command(self, ctx, subcommand=None, *args):
        if not self.has_permission(ctx.author):
            await ctx.send("❌ No tienes permiso para usar este comando.")
            return

        if not self.is_zhongli_enabled():
            await ctx.send("⚠️ El comando `zhongli` está deshabilitado actualmente.")
            return

        if not subcommand:
            await ctx.send(
                "⚠️ Uso correcto: `!zhongli <subcomando> [args]`, "
                "por ejemplo `!zhongli permisos [dar/quitar] 'rol' @usuario` o `!zhongli ping`"
            )
            return

        # Todo lo demás lo maneja SubcommandsService con manejo de errores
        try:
            await self.subcommands_service.handle(ctx, subcommand, *args)
        except Exception as e:
            print(f"⚠️ Error inesperado en Zhongli command: {e}")
            await ctx.send("⚠️ Ocurrió un error inesperado al procesar el comando.")

async def setup(bot):
    await bot.add_cog(Zhongli(bot))
