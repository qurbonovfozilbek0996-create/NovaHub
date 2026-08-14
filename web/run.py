import multiprocessing
import os

import uvicorn


def run_web():
    port = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
    )


def run_bot():
    from app.bot import dp, bot
    import asyncio

    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    web_process = multiprocessing.Process(target=run_web)
    bot_process = multiprocessing.Process(target=run_bot)

    web_process.start()
    bot_process.start()

    web_process.join()
    bot_process.join()
