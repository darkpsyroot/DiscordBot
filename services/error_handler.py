# services/error_handler.py
import asyncio

class ErrorHandler:
    def __init__(self, prefix="⚠️ Error"):
        self.prefix = prefix

    async def wrap(self, func, ctx, *args, **kwargs):
        """
        Ejecuta func(*args, **kwargs) de manera segura.
        Si ocurre un error, lo imprime y envía mensaje a Discord.
        """
        try:
            await func(ctx, *args, **kwargs)
        except asyncio.CancelledError:
            # Permitir que cancelaciones de tareas no se traten como errores
            raise
        except Exception as e:
            print(f"{self.prefix} en {func.__name__}: {e}")
            try:
                await ctx.send(f"{self.prefix} al ejecutar `{func.__name__}`. Revisa los logs.")
            except Exception:
                # Evitar errores si ctx.send falla
                pass
