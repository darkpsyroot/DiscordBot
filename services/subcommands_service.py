# services/subcommands_service.py
import discord
from discord.ext import commands

class SubcommandsService:
    def __init__(self, cog):
        self.cog = cog
        self.subcommands = {
            "permisos": self.handle_permisos,
            "stop": self.handle_stop,
            "ping": self.handle_ping,
        }

    async def handle(self, ctx, subcommand, *args):
        func = self.subcommands.get(subcommand.lower())
        if func:
            await func(ctx, *args)
        else:
            await ctx.send(f"❓ No entiendo qué quieres hacer: `{subcommand}`")

    async def handle_permisos(self, ctx, *args):
        try:
            if len(args) < 3:
                await ctx.send("❌ Uso: `!mavuika permisos [dar/quitar] 'nombre_del_rol' @usuario`")
                return

            action = args[0].lower()
            role_name = args[1].strip("'\"")
            member = ctx.message.mentions[0] if ctx.message.mentions else None

            if not member:
                await ctx.send("❌ Debes mencionar a un usuario.")
                return

            if role_name.lower() == "arconte":
                await ctx.send("🚫 Solo Liserk puede modificar el rol de **Arconte**.")
                return

            permisos_cog = self.cog.bot.get_cog("PermisosHandler")
            if not permisos_cog:
                await ctx.send("⚠️ Error: el sistema de permisos no está cargado.")
                return

            if action == "dar":
                await permisos_cog.dar_rol(ctx, role_name, member)
            elif action == "quitar":
                await permisos_cog.quitar_rol(ctx, role_name, member)
            else:
                await ctx.send("❌ Acción no reconocida. Usa `dar` o `quitar`.")
        except Exception as e:
            await ctx.send(f"⚠️ Ocurrió un error inesperado: {e}")

    async def handle_stop(self, ctx, *args):
        await ctx.send("🛑 El bot se apagará.")
        await self.cog.bot.close()

    async def handle_ping(self, ctx, *args):
        await ctx.send(f"🏓 Pong! Latencia: {round(self.cog.bot.latency * 1000)}ms")
