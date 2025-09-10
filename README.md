# JeetKesH
A Crypto Based project


## TODO:



# _bot_lock = asyncio.Lock()

# async def get_caller_count(client: TelegramClient, contract_address: str) -> int:
#     bot_username="@CallAnalyserBot"
#     async with _bot_lock:
#         try:
#             async with client.conversation(bot_username, timeout=2) as conv:
#                 try:
#                     await conv.send_message(contract_address)
#                     response = await asyncio.wait_for(
#                             conv.get_response(),
#                             timeout=2
#                         )
#                     if not isinstance(response):
#                         raise ValueError("Invalid response type")
#                     text = response.text.strip()
#                     if "wrong CA" in text or "no call" in text:
#                         return 0
#                     if 'received calls from' in text:
#                         match = re.search(r'(\d+) callers', text)
#                         if match:
#                             return int(match.group(1))
#                     raise ValueError(f"Unrecognized response: {text}")
#                 except asyncio.TimeoutError:
#                     await asyncio.sleep(0.5)  
#         except Exception as e:
#             print(f"Caller count failed for {contract_address}: {type(e).__name__} - {str(e)}")
#             return 0