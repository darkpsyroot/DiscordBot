from discord.ext import commands
from services.audio_service import AudioService
from comandos import COMMANDS

class Audio (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.audio_service = AudioService()

        # Diccionario que mapea subcomando -> función
        self.audio_commands = {
            COMMANDS["audio1"]: self.audio1,
            COMMANDS["audio2"]: self.audio2,
            COMMANDS["audio3"]: self.audio3,
        }

    async def handle(self, ctx, subcommand):
        func = self.audio_commands.get(subcommand.lower())
        if func:
            try:
                await func(ctx)
            except Exception as e:
                print(f"⚠️ Error ejecutando audio {subcommand}: {e}")
                await ctx.send("⚠️ Ocurrió un error al intentar reproducir el audio.")
        else:
            await ctx.send(f"❌ Subcomando de audio desconocido: `{subcommand}`")

    # Métodos individuales de cada audio
    async def audio1(self, ctx):
        await self.audio_service.enviar_audio(ctx, "assets/audio/gritoescoffier.mp3")

    async def audio2(self, ctx):
        await self.audio_service.enviar_audio(ctx, "assets/audio/navia_fire.mp3")

    async def audio3(self, ctx):
        await self.audio_service.enviar_audio(ctx, "assets/audio/FurinaSama.mp3")

async def setup(bot):
    await bot.add_cog(Audio(bot))
