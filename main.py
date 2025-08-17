import discord
from discord.ext import commands
import asyncio
import pathlib
from config import DISCORD_TOKEN, COMMAND_PREFIX, GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None, intents=intents)

async def load_cogs():
    base_path = pathlib.Path('./cogs').resolve()
    for filepath in base_path.rglob('*.py'):
        if filepath.name == '__init__.py':
            continue
        try:
            relative_path = filepath.relative_to(base_path.parent)
            module = '.'.join(relative_path.with_suffix('').parts)
            print(f"Cargando extensión: {module}")  # Para debug
            await bot.load_extension(module)
        except Exception as e:
            print(f"⚠️ Error cargando cog {filepath}: {e}")

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print('📦 Comandos cargados')
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"🌐 Sincronizados {len(synced)} comandos slash en el servidor {GUILD_ID}.")
    except Exception as e:
        print(f"⚠️ Error sincronizando comandos slash: {e}")

async def main():
    try:
        async with bot:
            await load_cogs()
            await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"⚠️ Error crítico iniciando el bot: {e}")

# Check global para deshabilitar el bot salvo Mavuika
@bot.check
async def global_bot_enabled(ctx):
    try:
        mavuika_cog = bot.get_cog("Mavuika")

        # Cog del comando actual (si existe)
        cog_name = ctx.command.cog_name if ctx.command else None

        # Si el bot está deshabilitado y no es Mavuika, bloqueamos
        if mavuika_cog and not mavuika_cog.bot_enabled and cog_name != "Mavuika":
            await ctx.send("🚫 Todos los comandos del bot están desactivados temporalmente.")
            return False

        return True
    except Exception as e:
        print(f"⚠️ Error en global_bot_enabled: {e}")
        return False

asyncio.run(main())
