from discord.ext import commands
from services.test_service import TestService
from comandos import COMMANDS

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.test_service = TestService()

    @commands.group(name="test", invoke_without_command=True)
    async def test(self, ctx):
        await ctx.send("Usa un subcomando, por ejemplo !test ping")

    @test.command(name=COMMANDS["ping"])
    async def ping(self, ctx):
        await self.test_service.ping_response(ctx)

async def setup(bot):
    await bot.add_cog(Test(bot))
