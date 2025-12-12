from discord.ext import commands
from services.media_service import MediaService
from comandos import COMMANDS

class White(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.media_service = MediaService()

        self.white_commands = {
            COMMANDS["white1"]: self.white1
        }

    async def handle(self, ctx, subcommand=None):
        if not subcommand:
            await ctx.send(f"❌ Uso: `!<furina|mavuika> white {COMMANDS['white1']}`")
            return

        func = self.white_commands.get(subcommand.lower())
        if func:
            try:
                await func(ctx)
            except Exception as e:
                print(f"⚠️ Error ejecutando white {subcommand}: {e}")
                await ctx.send("⚠️ Ocurrió un error al ejecutar el comando white.")
        else:
            await ctx.send(f"❌ Subcomando de white desconocido: `{subcommand}`")

    async def white1(self, ctx):
        await self.media_service.enviar_foto_y_audio(
            ctx,
            "assets/imagenes/grr.jpeg",
            "assets/audio/onlygrr.mp4"
        )

async def setup(bot):
    await bot.add_cog(White(bot))
