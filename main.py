import discord
from discord.ext import commands
import asyncio
import pathlib
from config import DISCORD_TOKEN, COMMAND_PREFIX, GUILD_ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None, intents=intents)

async def load_cogs():
    base_path = pathlib.Path('./cogs').resolve()
    for filepath in base_path.rglob('*.py'):
        if filepath.name == '__init__.py':
            continue
        
        relative_path = filepath.relative_to(base_path.parent)
        module = '.'.join(relative_path.with_suffix('').parts)
        
        print(f"Cargando extensión: {module}")  # Para debug
        
        await bot.load_extension(module)
"""
async def load_cogs():
    await bot.load_extension("cogs.generales.ping")
    await bot.load_extension("cogs.extras.gritoEscoffier")
    await bot.load_extension("cogs.personajes.zhongli")
"""

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    print('📦 Comandos cargados')
    guild = discord.Object(id=GUILD_ID)
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🌐 Sincronizados {len(synced)} comandos slash en el servidor {GUILD_ID}.")
    except Exception as e:
        print(f"⚠️ Error sincronizando comandos slash: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())
