import discord
from discord.ext import commands

class AutoRol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role_name = "Traveler"
        role = discord.utils.get(member.guild.roles, name=role_name)

        if role:
            await member.add_roles(role)
            print(f"✅ Rol '{role_name}' asignado a {member.name}")
        else:
            print(f"⚠️ No se encontró el rol '{role_name}'")

async def setup(bot):
    await bot.add_cog(AutoRol(bot))
