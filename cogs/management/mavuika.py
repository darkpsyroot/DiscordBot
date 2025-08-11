# cogs/management/mavuika.py
import discord
from discord.ext import commands
from services.subcommands_service import SubcommandsService

class Mavuika(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.required_role = "Arconte"
        self.subcommands_service = SubcommandsService(self)
        self.zhongli_enabled = True

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

        # Maneja otros subcomandos con el servicio
        await self.subcommands_service.handle(ctx, subcommand, *args)

    # Puedes agregar aquí otros métodos específicos si quieres

async def setup(bot):
    await bot.add_cog(Mavuika(bot))
