from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import os

# Replace with your values
API_ID = 22510712  # Your API ID from https://my.telegram.org
API_HASH = 'c715730ad25a64ea54448326dd78c028'  # Your API Hash from https://my.telegram.org
SESSION_FILE = 'jeetkesh.session'  # Without path if in same dir

# Create client using existing session
client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

async def get_otp_message():
    await client.start()
    # Search for Telegram official messages (OTP may come from there)
    entity = await client.get_entity('Telegram')  # or 'Telegram' or '@Telegram'
    history = await client(GetHistoryRequest(
        peer=entity,
        limit=10,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    for msg in history.messages:
        print(f"[{msg.date}] {msg.message}")

with client:
    client.loop.run_until_complete(get_otp_message())
