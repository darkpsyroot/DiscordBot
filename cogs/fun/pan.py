from discord.ext import commands
from services.media_service import MediaService
from comandos import COMMANDS

class Pan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.media_service = MediaService()

        self.pan_commands = {
            COMMANDS["pan1"]: self.pan1
        }

    async def handle(self, ctx, subcommand=None):
        if not subcommand:
            await ctx.send(f"❌ Uso: `!<furina|mavuika> pan {COMMANDS['pan1']}`")
            return

        func = self.pan_commands.get(subcommand.lower())
        if func:
            try:
                await func(ctx)
            except Exception as e:
                print(f"⚠️ Error ejecutando pan {subcommand}: {e}")
                await ctx.send("⚠️ Ocurrió un error al ejecutar el comando pan.")
        else:
            await ctx.send(f"❌ Subcomando de pan desconocido: `{subcommand}`")

    async def pan1(self, ctx):
        await self.media_service.enviar_foto_y_audio(
            ctx,
            "assets/imagenes/tiburoncin.jpg",
            "assets/audio/tiburoncin.mp3"
        )

async def setup(bot):
    await bot.add_cog(Pan(bot))
