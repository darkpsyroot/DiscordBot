class TestService:
    async def ping_response(self, destino):
        await destino.send('Pong!')
