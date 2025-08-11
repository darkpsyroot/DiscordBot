import discord

class VideoService:
    async def enviar_video(self, destino, video_path):
        try:
            await destino.send(file=discord.File(video_path))
        except Exception as e:
            print(f"Error enviando video {video_path}: {e}")
            await destino.send("No pude enviar el video, hubo un error.")

    async def enviar_enlace(self, destino, url):
        try:
            await destino.send(url)
        except Exception as e:
            print(f"Error enviando enlace {url}: {e}")
            await destino.send("No pude enviar el enlace, hubo un error.")
