from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del archivo .env

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX = "!"
GUILD_ID = 1391975621764317284
