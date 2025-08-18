from discord.ext import commands
from services.video_service import VideoService
from comandos import COMMANDS


class Video (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.video_service = VideoService()

        # Diccionario que mapea subcomando -> función
        self.video_commands = {
            COMMANDS["video1"]: self.video1,
            COMMANDS["video2"]: self.video2,
            COMMANDS["video3"]: self.video3,
            COMMANDS["video4"]: self.video4,
            COMMANDS["video5"]: self.video5,
            COMMANDS["video6"]: self.video6,
            COMMANDS["video7"]: self.video7,
            COMMANDS["video8"]: self.video8,
            COMMANDS["video9"]: self.video9,
            COMMANDS["video10"]: self.video10,
            COMMANDS["video11"]: self.video11,
        }

    async def handle(self, ctx, subcommand):
        func = self.video_commands.get(subcommand.lower())
        if func:
            await func(ctx)
        else:
            await ctx.send(f"❌ Subcomando de video desconocido: `{subcommand}`")

    # Métodos individuales de cada video
    async def video1(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/BestTeam.mp4")

    async def video2(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/Hapapa.mp4")

    async def video3(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/AliRun.mp4")

    async def video4(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/RicaCola.mp4")

    async def video5(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/Face.mp4")

    async def video6(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/FuriTao.mp4")

    async def video7(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/lesbiandowsky.mp4")

    async def video8(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/MavuikaMyLove.mp4")

    async def video9(self, ctx):
        await self.video_service.enviar_enlace(ctx, "https://www.youtube.com/watch?v=gh6gtpH4EbQ&list=RDgh6gtpH4EbQ&start_radio=1&ab_channel=Stormz67")

    async def video10(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/Cancer.mp4")

    async def video11(self, ctx):
        await self.video_service.enviar_video(ctx, "assets/video/PollitoConPapas.mp4")

async def setup(bot):
    await bot.add_cog(Video(bot))

