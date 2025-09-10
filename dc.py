import discord
import yaml
from discord.ext import commands
import time 
from dataset import SimpleCAFilter
import json
from io import BytesIO
from utils import get_token_data, create_jeet_card, create_TA_card

tier_mapping = {
    # gold tier (1)
    "jsdao": 1,
    "bossmancallsofficial": 1,
    "apenow": 1,
    "gollumsgems": 1,
    "smokeyscalls": 1,
    "degenseals": 1,
    "alphagukesh": 1,
    "metadevcalls": 1,

    # silver tier (2)
    "ethgambles": 2,
    "parzicalls": 2,

    # bronze tier (3)
    "kolscope": 3,
    "callanalysersol": 3,
    "alexgambles": 3,
    "de/cap (open)": 3,
    "itachidegencalls": 3,
    "wifechangingcallss": 3,
    "ch1ro0": 3,
    "callanalyserbot": 3,
    "callanalyser2": 3,
    "metadevflexca": 3,
}

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

async def start_discord_sender(queue):
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix="!", intents=intents)
    ca_cache = SimpleCAFilter(max_size=30)

    @bot.event
    async def on_ready():
        print(f"Discord bot logged in as {bot.user}")

        while True:
            dets = await queue.get()
            detail = json.loads(dets)
            try:            
                # send TA messages to gold channel with imgs
                if detail['type']=='ta':
                    source = detail["source"]
                    raw_msg = detail["raw"]
                    img_hex_list = detail.get("images", [])
                    print(len(img_hex_list))

                    embed = await create_TA_card({
                        "source": source,
                        "raw": raw_msg
                    })
                    print("⚡ embed ready")
                    channel = bot.get_channel(config["discord"]["1_id"])
                    
                    # ✅ Handle one or more image files
                    files = []
                    for i, hex_img in enumerate(img_hex_list):
                        image_bytes = bytes.fromhex(hex_img)
                        file = discord.File(fp=BytesIO(image_bytes), filename=f"img_{i+1}.jpg")
                        files.append(file)

                        if i == 0:  # Attach first image to embed
                            embed.set_image(url=f"attachment://img_{i+1}.jpg")
                    try:
                        await channel.send(embed=embed, files=files)
                        print("✅✅✅ Sent to Discord")
                    except Exception as e:
                            print(f"❌❌ Discord send failed: {e}")

                # send messages to their respectful channel
                else:
                    source = detail["source"]
                    ca = detail["contract"]
                    calls = detail["calls"]
                    raw = detail["raw"]
                    # print("checking if new token or not")
                    # so even if the token is not new it will be send if it is called by silver or gold channel
                   
                    tier = tier_mapping.get(source.lower(), 3)
                    if tier == 3:
                        if await ca_cache.should_skip(ca.lower()):
                            print(f"🟡 Skipping duplicate CA: {ca}")
                            continue
                    
                    print("getting token data")
                    # Get rest of the data for the ca using dex api
                    data = await get_token_data(ca)
                    if not data:
                        print(f"❌ Skipping invalid contract: {ca}")
                        continue
                    data['tier'] = tier
                    data['source'] = source
                    data['calls'] = calls
                    # Print the token data
                    print("📦 Token Data:")
                    for key, val in data.items():
                        print(f" - {key}: {val}")
                    print("-" * 50)

                    # Create the dc message
                    message = await create_jeet_card(data)
                    channel = bot.get_channel(config["discord"][f"{data['tier']}_id"])
                    if not message:
                        print("⛔ Message error ")
                        continue
                    
                    # TRY to send the message to dc and catch for error
                    try: 
                        message = await channel.send(embed=message)
                        await message.add_reaction('<a:watch:1380744932750528613>')
                        print(f"✅ Forwarded to Discord")

                    except Exception as e:
                        print(f"❌ Discord send failed: {e}")
            
            except Exception as e:
                print(f"🔥 Error processing message: {dets} — {e}") 

    await bot.start(config["discord"]["bot_token"])