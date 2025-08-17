import os
from openai import AsyncOpenAI

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def ask(self, question: str) -> str:
        """Envía la pregunta a OpenAI y devuelve la respuesta."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": question}],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️ Error al consultar OpenAI: {e}"
