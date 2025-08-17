from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del archivo .env

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
COMMAND_PREFIX = "!"
GUILD_ID = 1391975621764317284
