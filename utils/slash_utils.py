from discord import app_commands, Interaction, File, Object

def crear_comando_slash(bot, nombre_comando, numero, ruta, guild_id, enviar_imagen_func):
    async def slash(interaction: Interaction):
        await enviar_imagen_func(interaction, numero)

    slash.__name__ = f"zhongli_zh{numero}_slash"

    comando = app_commands.Command(
        name=nombre_comando,
        description=f"Zhongli imagen {numero}",
        callback=slash,
    )
    bot.tree.add_command(comando, guild=Object(id=guild_id))
