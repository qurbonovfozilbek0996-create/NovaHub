import multiprocessing
import uvicorn


def run_web():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
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
