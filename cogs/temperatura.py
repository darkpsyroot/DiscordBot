import aiohttp
from discord.ext import commands
from comandos import COMMANDS
import discord

class TemperaturaHelper:
    @staticmethod
    async def obtener_temperaturas():
        # Coordenadas de las ciudades
        ciudades = {
            "🇪🇸 España - Huelva": (37.27, -6.94),
            "🇦🇷 Argentina - Buenos Aires": (-34.61, -58.38),
            "🇧🇷 Brasil - São Paulo": (-23.55, -46.63),
            "🇲🇽 México - CDMX": (19.43, -99.13),
            "🇲🇽 México - Sinaloa": (24.80, -107.39)
        }

        url_base = "https://api.open-meteo.com/v1/forecast"

        resultados = []
        async with aiohttp.ClientSession() as session:
            for nombre, (lat, lon) in ciudades.items():
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": True
                }

                try:
                    async with session.get(url_base, params=params) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            temp = data["current_weather"]["temperature"]
                            resultados.append(f"{nombre}: **{temp}°C** 🌡️")
                        else:
                            resultados.append(f"{nombre}: ⚠️ Error al obtener datos")
                except Exception as e:
                    resultados.append(f"{nombre}: ⚠️ Error ({e})")

        return resultados


class Temperatura(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMANDS["temperatura"])
    async def temperatura(self, ctx):
        try:
            temperaturas = await TemperaturaHelper.obtener_temperaturas()

            embed = discord.Embed(
                title="🌤️ Temperaturas actuales",
                description="\n".join(temperaturas),
                color=discord.Color.orange()
            )
            # embed.set_footer(text="Solicitado por " + ctx.author.display_name)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Error en `temperatura`: {e}")

async def setup(bot):
    await bot.add_cog(Temperatura(bot))
