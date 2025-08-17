import discord
from discord.ext import commands
from services.subcommands_service import SubcommandsService
from services.openai_service import OpenAIService

class Furina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.openai_service = OpenAIService()
        self.subcommands_service = SubcommandsService(self, self.openai_service)

    @commands.command(name="furina")
    async def furina_command(self, ctx, subcommand=None, *args):
        if not subcommand:
            await ctx.send("❌ Uso: `!furina <subcomando>`")
            return
        
        # Manejo de errores para que no truene
        try:
            await self.subcommands_service.handle(ctx, subcommand, *args)
        except Exception as e:
            print(f"⚠️ Error inesperado en Furina command: {e}")
            await ctx.send("⚠️ Ocurrió un error inesperado al procesar el comando.")

async def setup(bot):
    await bot.add_cog(Furina(bot))
