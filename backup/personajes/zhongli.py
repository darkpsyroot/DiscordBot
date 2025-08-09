import os
import discord
from discord.ext import commands
from discord import app_commands, Interaction, File
from comandos import COMMANDS
from config import GUILD_ID
from utils.slash_utils import crear_comando_slash

class Zhongli(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.folder_path = "assets/imagenes/Paimon_s Paintings/Set 3/"

    async def enviar_imagen(self, destino, numero):
        ruta = f"{self.folder_path}Zhongli {numero}.png"
        if isinstance(destino, Interaction):
            await destino.response.send_message(file=File(ruta))
        else:
            await destino.send(file=File(ruta))

    async def cog_load(self):
        """Se ejecuta automáticamente al cargar el cog."""
        for filename in os.listdir(self.folder_path):
            if filename.startswith("Zhongli") and filename.endswith(".png"):
                try:
                    numero = int(filename.split(" ")[1].split(".")[0])
                except ValueError:
                    continue

                key = f"zhongli_zh{numero}"
                if key not in COMMANDS:
                    continue

                nombre_comando = COMMANDS[key]

                # Prefijo (!zh1)
                async def prefijo(ctx, num=numero):
                    await self.enviar_imagen(ctx, num)

                prefijo.__name__ = f"zhongli_zh{numero}_command"
                setattr(self, prefijo.__name__, commands.command(name=nombre_comando)(prefijo))

                # Slash (/zh1) usando la función de utilidad
                crear_comando_slash(
                    bot=self.bot,
                    nombre_comando=nombre_comando,
                    numero=numero,
                    ruta=self.folder_path,
                    guild_id=GUILD_ID,
                    enviar_imagen_func=self.enviar_imagen
                )

async def setup(bot):
    await bot.add_cog(Zhongli(bot))
