# cogs/furina.py
from discord.ext import commands
import os
#from dotenv import load_dotenv
from config import OPENAI_API_KEY
from openai import OpenAI
from comandos import COMMANDS

client_openai = OpenAI(api_key=OPENAI_API_KEY)

class Furina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activa = True

    @commands.command(name="furina")
    async def furina(self, ctx, *, argumento: str = None):
        # Solo usuarios con rol "Arconte" pueden usar estos comandos especiales
        autor_tiene_rol = any(role.name == "Arconte" for role in ctx.author.roles)

        if argumento is None:
            if not self.activa:
                # Furina está dormida y no responde preguntas
                return
            await ctx.send("Por favor, hazme una pregunta después del comando. Ejemplo: `!furina ¿qué hora es?`")
            return

        argumento_lower = argumento.lower()

        if argumento_lower == COMMANDS["furina_sleep"]:
            if autor_tiene_rol:
                self.activa = False
                await ctx.send("Durmiendo...")
            else:
                await ctx.send("Solo Liserk puede hacer que duerma.")
            return

        if argumento_lower == COMMANDS["furina_wake"]:
            if autor_tiene_rol:
                self.activa = True
                await ctx.send("Buenassss.")
            else:
                await ctx.send("Solo Liserk puede despertarme.")
            return

        # Si no es un comando especial, y Furina está dormida, no responde
        if not self.activa:
            # Cuando duerme, no responde
            return

        # Responder pregunta normal con OpenAI
        try:
            respuesta = client_openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un bot útil y divertido en Discord."},
                    {"role": "user", "content": argumento}
                ]
            )
            contenido = respuesta.choices[0].message.content
            await ctx.send(contenido)
        except Exception as e:
            await ctx.send(f"Error al consultar OpenAI: {e}")

async def setup(bot):
    await bot.add_cog(Furina(bot))
