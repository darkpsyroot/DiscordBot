import discord

class AudioService:
    async def enviar_audio(self, destino, audio_path):
        await destino.send(
            files=[
                discord.File(audio_path)
            ]
        )
