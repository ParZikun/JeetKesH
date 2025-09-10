from telethon.sync import TelegramClient, events
import re
import time
import yaml
import asyncio
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from io import BytesIO
import json

gold_tier =[
    "jsdao",
    "bossmancallsofficial",
    "apenow",
    "gollumsgems",
    "smokeyscalls",
    "degenseals",
    "alphagukesh"
]

# async def get_caller_count(client: TelegramClient, contract_address: str) -> int:
#     bot_username="@CallAnalyserBot"
#     try:
#         async with client.conversation(bot_username, timeout=5) as conv:
#             await client.send_message(bot_username, contract_address)
#             response = await conv.get_response()
#             match = re.search(r'❇️\(Total Call\)🚀 \$.+ received calls from (\d+) callers', response.text)
#             return int(match.group(1)) if match else 0
#     except asyncio.TimeoutError:
#         print("Timeout waiting for bot response")
#     except Exception as e:
#         print(f"Error getting caller count: {e}")
#     return 0

async def start_telegram_listener(queue):
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    client = TelegramClient(
        config["telegram"]["session_name"],
        config["telegram"]["api_id"],
        config["telegram"]["api_hash"]
    )
    
    CONTRACT_REGEX = re.compile(r'\b[0-9a-zA-Z]{30,44}\b')

    @client.on(events.NewMessage(chats=config["telegram"]["channels"]))
    async def handler(event):
        if not event.message:
            return
        
        contract = CONTRACT_REGEX.findall(event.message.text)
        source = event.chat.username or event.chat.title
        source = source.lower()

        
        # if we have a call with ca
        if contract:
            contract = contract[0]
            # caller_count = await get_caller_count(client,contract)
            caller_count = "TODO"
            clean_msg = json.dumps({
                "type": "ca",
                "source": source,
                "contract": contract,
                "calls": caller_count,
                "raw": event.message.text
            })
                
            # f"{source}|{contract}|{caller_count}|{event.message.text}"
            print("TG: ", clean_msg)
            await queue.put(clean_msg)
        # if we have a TA with chart img and some text along with it
        elif source in gold_tier:
            try: 
                image_bytes_list = []
                
                # ✅ Support multiple images (media group or forward album logic if needed)
                if event.message.media and isinstance(event.message.media, (MessageMediaPhoto, MessageMediaDocument)):
                    image_stream = BytesIO()
                    await event.message.download_media(file=image_stream)
                    image_bytes = image_stream.getvalue()
                    image_bytes_list.append(image_bytes.hex())  # hex encode for transport

                clean_msg = json.dumps({
                    "type": "ta",
                    "source": source,
                    "raw": event.message.message,
                    "images": image_bytes_list
                })

                print("TG:", clean_msg)
                await queue.put(clean_msg)

                # if event.message.media and isinstance(event.message.media, MessageMediaPhoto):
                #     image_stream = BytesIO()
                #     await event.message.download_media(file=image_stream)
                #     image_bytes=image_stream.getvalue()
                #     clean_msg = (f"{source}|{event.message.text}|{image_bytes.hex()}")
                #     print("TG: ", event.message.text)
                #     await queue.put(clean_msg)
            except Exception as e:
                print(f"Failed to process media: {e}")


    await client.start()
    print("Telegram listener started...")
    await client.run_until_disconnected()
