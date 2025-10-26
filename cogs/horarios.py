import pytz
from datetime import datetime
from discord.ext import commands
from comandos import COMMANDS
import discord

class HorariosHelper(commands.Cog):
    @staticmethod
    def obtener_horarios():
        zonas = {
            "🇦🇷 Argentina": "America/Argentina/Buenos_Aires",
            "🇧🇷 Brasil": "America/Sao_Paulo",
            "🇲🇽 México (CDMX - UTC-6)": "America/Mexico_City",
            "🇲🇽 México (México - UTC-7)": "America/Hermosillo",
            "🇵🇪 Perú (UTC-5)": "America/Lima",
            "🇪🇸 España (UTC+1)": "Europe/Madrid",
            "🇨🇴 Colombia (UTC-5)": "America/Bogota"
        }

        # Orden alfabético
        zonas_ordenadas = dict(sorted(zonas.items(), key=lambda x: x[0]))

        horas = []
        for pais, zona in zonas_ordenadas.items():
            tz = pytz.timezone(zona)
            hora = datetime.now(tz).strftime("%H:%M:%S")
            horas.append(f"{pais}: **{hora}**")

        return horas


class Horarios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name=COMMANDS["horarios"])
    async def horarios(self, ctx):
        try:
            horas = HorariosHelper.obtener_horarios()

            embed = discord.Embed(
                title="🕒 Horarios actuales",
                description="\n".join(horas),
                color=discord.Color.blue()
            )
            #embed.set_footer(text="Solicitado por " + ctx.author.display_name)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Error en `horarios`: {e}")

async def setup(bot):
    await bot.add_cog(Horarios(bot))
