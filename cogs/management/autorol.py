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
            try:
                await member.add_roles(role)
                print(f"✅ Rol '{role_name}' asignado a {member.name}")
            except Exception as e:
                print(f"⚠️ Error asignando rol '{role_name}' a {member.name}: {e}")
        else:
            print(f"⚠️ No se encontró el rol '{role_name}'")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"⚠️ Miembro {member} salió o fue expulsado.")

async def setup(bot):
    await bot.add_cog(AutoRol(bot))
