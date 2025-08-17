# cogs/management/mavuika.py
import discord
from discord.ext import commands
from services.subcommands_service import SubcommandsService
from services.openai_service import OpenAIService
from comandos import COMMANDS  # <-- Importamos el diccionario

class Mavuika(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.required_role = "Arconte"
        self.openai_service = OpenAIService()  # instancia global compartida
        self.subcommands_service = SubcommandsService(self, self.openai_service)
        self.zhongli_enabled = True
        self.bot_enabled = True  # Flag global para activar/desactivar todos los comandos

    def has_required_role(self, member):
        return any(role.name == self.required_role for role in member.roles)
    
    @commands.command(name="mavuika")
    async def mavuika_command(self, ctx, subcommand=None, *args):
        if not self.has_required_role(ctx.author):
            await ctx.send("🚫 Solo Liserk ❤️ puede usar este comando.")
            return

        if not subcommand:
            await ctx.send("🔥 Dime bby qué necesitas ❤️☺️")
            return

        # Comando especial para habilitar/deshabilitar Zhongli
        if subcommand.lower() == "zhongli":
            if not args:
                await ctx.send("❌ Uso: `!mavuika zhongli [on/off]`")
                return
            action = args[0].lower()
            if action == "on":
                self.zhongli_enabled = True
                await ctx.send("✅ Comando `zhongli` habilitado.")
            elif action == "off":
                self.zhongli_enabled = False
                await ctx.send("⚠️ Comando `zhongli` deshabilitado.")
            else:
                await ctx.send("❌ Opción inválida. Usa `on` o `off`.")
            return

        # Control para shutdown/startup del bot desde el diccionario
        if subcommand.lower() in [COMMANDS["shutdown_bot"], COMMANDS["startup_bot"]]:
            action = subcommand.lower()

            # Verifica que sea Liserk
            if not self.has_required_role(ctx.author):
                await ctx.send("🚫 Solo Liserk puede usar este comando.")
                return

            # Apagar el bot
            if action == COMMANDS["shutdown_bot"]:
                if not self.bot_enabled:
                    await ctx.send("🛑 El bot ya estaba apagado.")
                else:
                    self.bot_enabled = False
                    await ctx.send("🛑 Todos los comandos del bot han sido desactivados temporalmente (excepto Mavuika).")

            # Encender el bot
            elif action == COMMANDS["startup_bot"]:
                if self.bot_enabled:
                    await ctx.send("✅ El bot ya estaba encendido.")
                else:
                    self.bot_enabled = True
                    await ctx.send("✅ Todos los comandos del bot han sido reactivados.")
            return

        # Todos los demás subcomandos se manejan mediante SubcommandsService
        try:
            await self.subcommands_service.handle(ctx, subcommand, *args)
        except Exception as e:
            print(f"⚠️ Error en Mavuika command: {e}")
            await ctx.send("⚠️ Ocurrió un error inesperado al ejecutar tu comando.")

async def setup(bot):
    await bot.add_cog(Mavuika(bot))
