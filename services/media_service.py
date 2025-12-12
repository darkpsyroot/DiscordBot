import os
import discord

class MediaService:
    async def enviar_foto_y_audio(self, destino, image_path: str, audio_path: str, content: str | None = None):
        files = []

        if image_path and os.path.exists(image_path):
            files.append(discord.File(image_path))
        if audio_path and os.path.exists(audio_path):
            files.append(discord.File(audio_path))

        if not files:
            await destino.send("⚠️ Error, no encontre los archivos.")
            return

        await destino.send(
            content=content or "",
            files=files
        )
