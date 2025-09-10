import asyncio
from telegram import start_telegram_listener
from dc import start_discord_sender

async def main():
    queue = asyncio.Queue(maxsize=50)

    await asyncio.gather(
        start_telegram_listener(queue),
        start_discord_sender(queue)
    )
if __name__ == "__main__":
    asyncio.run(main())