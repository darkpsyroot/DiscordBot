# services/subcommands_service.py
import discord
import aiohttp
from discord.ext import commands
from services.youtube_service import YouTubeService
from services.error_handler import ErrorHandler
from cogs.video.video import Video
from cogs.audio.audio import Audio
from cogs.horarios import HorariosHelper 
from cogs.comandos.commands_renderer import CommandsRenderer
#from services.commands_service import CommandsService
from comandos import COMMANDS

class SubcommandsService:
    def __init__(self, cog, openai_service=None):
        self.cog = cog
        self.openai_service = openai_service
        self.video_cog = Video(cog.bot)
        self.audio_cog = Audio(cog.bot)
        #self.horarios_cog = HorariosHelper(cog.bot)
        self.youtube_service = YouTubeService()
        #self.commands_service = CommandsService(cog.bot)
        self.error_handler = ErrorHandler(prefix="⚠️ Ocurrió un error")

        self.subcommands = {
            "permisos": self.handle_permisos,
            "stop": self.handle_stop,
            "ping": self.handle_ping,
            "expulsar": self.handle_expulsar,
            "banear": self.handle_banear,
            "gpt": self.handle_openai,
            "video": self.handle_video,
            "audio": self.handle_audio,
            "youtube": self.handle_youtube,
            "lista": self.handle_comandos,
            COMMANDS["horarios"]: self.handle_horarios,
            COMMANDS["temperatura"]: self.handle_temperatura

        }

    # ------------------ Helpers ------------------
    def has_any_role(self, member, role_names):
        return any(role.name in role_names for role in member.roles)

    # ------------------ Main handler ------------------
    async def handle(self, ctx, subcommand, *args):
        try:
            mavuika_cog = self.cog.bot.get_cog("Mavuika")
            if mavuika_cog and not mavuika_cog.bot_enabled and ctx.cog_name != "Mavuika":
                await ctx.send("🚫 Todos los comandos del bot están desactivados temporalmente.")
                return

            func = self.subcommands.get(subcommand.lower())
            if func:
                await self.error_handler.wrap(func, ctx, *args)
            else:
                await ctx.send(f"❓ No entiendo qué quieres hacer: `{subcommand}`")
        except Exception as e:
            print(f"⚠️ Error general en handle: {e}")
            await ctx.send("⚠️ Ocurrió un error inesperado al procesar tu comando.")

    # ---------------- Video Handler ----------------
    async def handle_video(self, ctx, *args):
        if not args:
            await ctx.send("❌ Uso: `!<comando> video <subcomando>`")
            return
        subcommand2 = args[0]
        await self.error_handler.wrap(self.video_cog.handle, ctx, subcommand2)
    
    # ---------------- Audio Handler ----------------
    async def handle_audio(self, ctx, *args):
        if not args:
            await ctx.send("❌ Uso: `!<comando> audio <subcomando>`")
            return

        subcommand2 = args[0]
        await self.error_handler.wrap(self.audio_cog.handle, ctx, subcommand2)

    # ---------------- Horarios Handler ----------------
    async def handle_horarios(self, ctx, *args):
        async def inner(ctx, *args):
            # Obtenemos el cog Horarios
            horarios_cog = self.cog.bot.get_cog("Horarios")
            if not horarios_cog:
                await ctx.send("⚠️ El cog de horarios no está cargado.")
                return

            # Llamamos directamente al comando de Horarios
            await horarios_cog.horarios(ctx)

        # Usamos ErrorHandler para capturar errores
        await self.error_handler.wrap(inner, ctx, *args)
    
    # ---------------- Temperatura Handler ----------------
        
    async def handle_temperatura(self, ctx, *args):
        async def inner(ctx, *args):
            ciudades = {
                "🇪🇸 España - Huelva": (37.27, -6.94),
                "🇦🇷 Argentina - Buenos Aires": (-34.61, -58.38),
                "🇧🇷 Brasil - São Paulo": (-23.55, -46.63),
                "🇲🇽 México - CDMX": (19.43, -99.13),
                "🇲🇽 México - Sinaloa": (24.80, -107.39)
            }

            url = "https://api.open-meteo.com/v1/forecast"
            resultados = []

            async with aiohttp.ClientSession() as session:
                for nombre, (lat, lon) in ciudades.items():
                    try:
                        async with session.get(url, params={
                            "latitude": lat,
                            "longitude": lon,
                            "current_weather": "true"  # 🔥 CORREGIDO: string, no boolean
                        }) as resp:
                            if resp.status == 200:
                                data = await resp.json()
                                weather = data.get("current_weather")
                                if weather and "temperature" in weather:
                                    temp = weather["temperature"]
                                    resultados.append(f"{nombre}: **{temp}°C** 🌡️")
                                else:
                                    resultados.append(f"{nombre}: ⚠️ Sin datos de temperatura")
                            else:
                                resultados.append(f"{nombre}: ⚠️ Error {resp.status} al obtener datos")
                    except Exception as e:
                        resultados.append(f"{nombre}: ⚠️ Error ({e})")

            embed = discord.Embed(
                title="🌤️ Temperaturas actuales",
                description="\n".join(resultados),
                color=discord.Color.orange()
            )

            await ctx.send(embed=embed)

        await self.error_handler.wrap(inner, ctx, *args)
    # ---------------- Comandos Handler ----------------
    async def handle_comandos(self, ctx, *args):
        async def inner(ctx, *args):
            if not args or args[0].lower() != "comandos":
                await ctx.send(f"❌ Subcomando desconocido: `{args[0]}`" if args else "❌ Uso: `!<comando> comandos lista`")
                return

            # Cog que invoca el comando
            cog_name = ctx.command.cog_name.lower()

            # Solo estos cogs pueden listar sus comandos
            if cog_name not in ["furina", "mavuika", "zhongli"]:
                await ctx.send("❌ No puedes listar comandos de este cog.")
                return

            renderer = CommandsRenderer(self.cog.bot)
            texto = await renderer.render_for_user(ctx.author, cog_name=cog_name, prefix=ctx.prefix)
            await ctx.send(texto)

        # Usamos ErrorHandler para capturar errores
        await self.error_handler.wrap(inner, ctx, *args)

    # ------------ OPENAI ------------------
    async def handle_openai(self, ctx, *args):
        if not args:
            await ctx.send(f"❌ Uso: `!mavuika openai <pregunta|{COMMANDS['furina_sleep']}|{COMMANDS['furina_wake']}>`")
            return

        command = args[0].lower()

        # Comandos de control usando el diccionario
        if command == COMMANDS["furina_sleep"]:
            if self.has_any_role(ctx.author, ["Arconte"]):
                self.openai_service.activa = False
                await ctx.send("😴 OpenAI está ahora dormida.")
            else:
                await ctx.send("🚫 Solo Liserk puede dormir a OpenAI.")
            return

        if command == COMMANDS["furina_wake"]:
            if self.has_any_role(ctx.author, ["Arconte"]):
                self.openai_service.activa = True
                await ctx.send("🌞 OpenAI está despierta y lista para responder.")
            else:
                await ctx.send("🚫 Solo Liserk puede despertar a OpenAI.")
            return

        # Si no es comando de control, es pregunta normal
        if not self.openai_service.activa:
            await ctx.send("😴 OpenAI está dormida, no puedo responder ahora.")
            return

        question = " ".join(args)
        #await ctx.send("🤔 Pensando...")
        try:
            answer = await self.openai_service.ask(question)
            await ctx.send(f"💡 {answer}")
        except Exception as e:
            print(f"⚠️ Error en OpenAI: {e}")
            await ctx.send("⚠️ Ocurrió un error al consultar OpenAI.")

    # ------------ YOUTUBE ------------------
    async def handle_youtube(self, ctx, *args):
        if len(args) < 1:
            await ctx.send("❌ Uso: `!furina youtube <consulta>`")
            return

        query = " ".join(args)
        try:
            videos = await self.youtube_service.search_video(query)
            if videos:
                video = videos[0]
                await ctx.send(f"📺 {video['title']} → {video['url']}")
            else:
                await ctx.send("⚠️ No encontré ningún resultado en YouTube.")
        except Exception as e:
            print(f"⚠️ Error en YouTube: {e}")
            await ctx.send(f"⚠️ Error buscando en YouTube: {e}")

    # ------------ PERMISOS -----------------
    async def handle_permisos(self, ctx, *args):
        async def inner(ctx, *args):
            if len(args) < 3:
                await ctx.send("❌ Uso: `!mavuika permisos [dar/quitar] 'nombre_del_rol' @usuario`")
                return

            action = args[0].lower()
            role_name = args[1].strip("'\"")
            member = ctx.message.mentions[0] if ctx.message.mentions else None

            if not member:
                await ctx.send("❌ Debes mencionar a un usuario.")
                return

            if role_name.lower() == "arconte":
                await ctx.send("🚫 Solo Liserk puede modificar el rol de **Arconte**.")
                return

            permisos_cog = self.cog.bot.get_cog("PermisosHandler")
            if not permisos_cog:
                await ctx.send("⚠️ Error: el sistema de permisos no está cargado.")
                return

            if action == "dar":
                await permisos_cog.dar_rol(ctx, role_name, member)
            elif action == "quitar":
                await permisos_cog.quitar_rol(ctx, role_name, member)
            else:
                await ctx.send("❌ Acción no reconocida. Usa `dar` o `quitar`.")

        await self.error_handler.wrap(inner, ctx, *args)

    # ------------ STOP ---------------------
    async def handle_stop(self, ctx, *args):
        if not self.has_any_role(ctx.author, ["Arconte"]):
            await ctx.send("🚫 Solo Liserk puede apagar el bot.")
            return

        await ctx.send("🛑 El bot se apagará por orden de Liserk.")
        try:
            await self.cog.bot.close()
        except Exception as e:
            print(f"⚠️ Error al cerrar bot: {e}")
            await ctx.send("⚠️ Ocurrió un error al apagar el bot.")

    # ------------ PING ---------------------
    async def handle_ping(self, ctx, *args):
        if not self.has_any_role(ctx.author, ["Arconte", "ZhongliSimp"]):
            await ctx.send("🚫 No tienes permisos para usar ping.")
            return
        await ctx.send(f"🏓 Pong! Latencia: {round(self.cog.bot.latency * 1000)}ms")

    # ------------ EXPULSAR -----------------
    async def handle_expulsar(self, ctx, *args):
        async def inner(ctx, *args):
            if not self.has_any_role(ctx.author, ["Arconte", "ZhongliSimp"]):
                await ctx.send("🚫 No tienes permisos para expulsar usuarios.")
                return

            if not ctx.message.mentions:
                await ctx.send("❌ Debes mencionar a un usuario para expulsarlo.")
                return

            member = ctx.message.mentions[0]
            reason = " ".join(args[1:]) if len(args) > 1 else "Sin motivo"
            try:
                await member.kick(reason=reason)
                await ctx.send(f"👢 {member.mention} fue expulsado. Motivo: {reason}")
            except Exception as e:
                print(f"⚠️ Error expulsando usuario: {e}")
                await ctx.send(f"⚠️ No pude expulsar al usuario: {e}")

        await self.error_handler.wrap(inner, ctx, *args)

    # ------------ BANEAR -------------------
    async def handle_banear(self, ctx, *args):
        async def inner(ctx, *args):
            if not self.has_any_role(ctx.author, ["Arconte", "ZhongliSimp"]):
                await ctx.send("🚫 No tienes permisos para banear usuarios.")
                return

            if not ctx.message.mentions:
                await ctx.send("❌ Debes mencionar a un usuario para banearlo.")
                return

            member = ctx.message.mentions[0]
            reason = " ".join(args[1:]) if len(args) > 1 else "Sin motivo"
            try:
                await member.ban(reason=reason, delete_message_days=1)
                await ctx.send(f"🔨 {member.mention} fue baneado. Motivo: {reason}")
            except Exception as e:
                print(f"⚠️ Error baneando usuario: {e}")
                await ctx.send(f"⚠️ No pude banear al usuario: {e}")

        await self.error_handler.wrap(inner, ctx, *args)
