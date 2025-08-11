from discord.ext import commands
import discord

class PermisosHandler(commands.Cog):  # ✅ Hereda de commands.Cog
    def __init__(self, bot):
        self.bot = bot

    async def dar_rol(self, ctx, role_name, member):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"❌ No encontré el rol `{role_name}`.")
            return
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ {member.mention} ahora tiene el rol **{role_name}**.")
        except discord.Forbidden:
            await ctx.send("🚫 No tengo permiso para asignar ese rol.")
        except discord.HTTPException as e:
            await ctx.send(f"⚠️ Error al asignar el rol: {e}")

    async def quitar_rol(self, ctx, role_name, member):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"❌ No encontré el rol `{role_name}`.")
            return
        try:
            await member.remove_roles(role)
            await ctx.send(f"✅ {member.mention} ya no tiene el rol **{role_name}**.")
        except discord.Forbidden:
            await ctx.send("🚫 No tengo permiso para quitar ese rol.")
        except discord.HTTPException as e:
            await ctx.send(f"⚠️ Error al quitar el rol: {e}")


async def setup(bot):
    await bot.add_cog(PermisosHandler(bot))  # ✅ Ahora sí será un Cog válido
