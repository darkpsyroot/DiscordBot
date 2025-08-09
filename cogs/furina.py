# cogs/furina.py
from discord.ext import commands
import os
#from dotenv import load_dotenv
from config import OPENAI_API_KEY
from openai import OpenAI

client_openai = OpenAI(api_key=OPENAI_API_KEY)

class Furina(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="furina")
    async def furina(self, ctx, *, pregunta: str = None):
        if pregunta is None:
            await ctx.send("Por favor, hazme una pregunta después del comando. Ejemplo: `!furina ¿qué hora es?`")
            return
        
        # Llamada a OpenAI
        try:
            respuesta = client_openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un bot útil y divertido en Discord."},
                    {"role": "user", "content": pregunta}
                ]
            )
            contenido = respuesta.choices[0].message.content
            await ctx.send(contenido)
        except Exception as e:
            await ctx.send(f"Error al consultar OpenAI: {e}")

async def setup(bot):
    await bot.add_cog(Furina(bot))
