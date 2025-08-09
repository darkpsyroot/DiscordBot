import discord

class VideoService:
    async def enviar_video(self, destino, video_path):
        await destino.send(
            file=discord.File(video_path)
        )
