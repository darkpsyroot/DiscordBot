from discord.ext import commands
from services.video_service import VideoService
from comandos import COMMANDS

class Video(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.video_service = VideoService()

    @commands.group(name="video", invoke_without_command=True)
    async def video(self, ctx):
        await ctx.send("Usa un subcomando, por ejemplo !video bestteam")

    @video.command(name=COMMANDS["video1"])
    async def video1(self, ctx):
        video_path = "assets/video/BestTeam.mp4"
        await self.video_service.enviar_video(ctx, video_path)
    
    @video.command(name=COMMANDS["video2"])
    async def video2(self, ctx):
        video_path = "assets/video/Hapapa.mp4"
        await self.video_service.enviar_video(ctx, video_path)
    
    @video.command(name=COMMANDS["video3"])
    async def video3(self, ctx):
        video_path = "assets/video/AliRun.mp4"
        await self.video_service.enviar_video(ctx, video_path)

    @video.command(name=COMMANDS["video4"])
    async def video4(self, ctx):
        video_path = "assets/video/RicaCola.mp4"
        await self.video_service.enviar_video(ctx, video_path)

    @video.command(name=COMMANDS["video5"])
    async def video5(self, ctx):
        video_path = "assets/video/Face.mp4"
        await self.video_service.enviar_video(ctx, video_path)

    @video.command(name=COMMANDS["video6"])
    async def video6(self, ctx):
        video_path = "assets/video/FuriTao.mp4"
        await self.video_service.enviar_video(ctx, video_path)

    @video.command(name=COMMANDS["video7"])
    async def video7(self, ctx):
        video_path = "assets/video/lesbiandowsky.mp4"
        await self.video_service.enviar_video(ctx, video_path)
    
    @video.command(name=COMMANDS["video8"])
    async def video8(self, ctx):
        video_path = "assets/video/MavuikaMyLove.mp4"
        await self.video_service.enviar_video(ctx, video_path)

async def setup(bot):
    await bot.add_cog(Video(bot))
