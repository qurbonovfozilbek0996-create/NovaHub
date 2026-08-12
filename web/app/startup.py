import asyncio

import uvicorn

from app.bot import dp, bot


async def start_bot():
    await dp.start_polling(bot)


async def start_web():
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

    server = uvicorn.Server(config)
    await server.serve()


async def run():
    await asyncio.gather(
        start_web(),
        start_bot(),
    )

if __name__ == "__main__":
    asyncio.run(run())
