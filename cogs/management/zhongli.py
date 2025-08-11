import discord
from discord.ext import commands
from .permisos_handler import PermisosHandler
from services.subcommands_service import SubcommandsService

class Zhongli(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = {"Arconte", "ZhongliSimp"}
        self.permisos_handler = PermisosHandler(bot)
        self.subcommands_service = SubcommandsService(self)

    def has_permission(self, member):
        return any(role.name in self.allowed_roles for role in member.roles)

    def is_zhongli_enabled(self):
        mavuika = self.bot.get_cog("Mavuika")
        return mavuika.zhongli_enabled if mavuika else True

    @commands.command()
    async def zhongli(self, ctx, subcommand=None, *args):
        if not self.has_permission(ctx.author):
            await ctx.send("❌ No tienes permiso para usar este comando.")
            return

        if not self.is_zhongli_enabled():
            await ctx.send("⚠️ El comando `zhongli` está deshabilitado actualmente.")
            return

        if subcommand is None:
            await ctx.send("⚠️ Uso correcto: `!zhongli permisos [dar/quitar] 'nombre_del_rol' @usuario` o `!zhongli ping`")
            return

        try:
            await self.subcommands_service.handle(ctx, subcommand, *args)
        except Exception as e:
            await ctx.send(f"⚠️ Error inesperado al procesar el comando: {e}")

async def setup(bot):
    await bot.add_cog(Zhongli(bot))
