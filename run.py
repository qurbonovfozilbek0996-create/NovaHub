import asyncio
import logging

from app.core.bot import bot
from app.core.dispatcher import dispatcher


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
