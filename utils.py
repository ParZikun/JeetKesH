import aiohttp
import discord
from discord import Embed, Colour, ButtonStyle, ActionRow, Button
from datetime import datetime

CHAIN_EMOJIS = {
    "ethereum": "<:eth:1381357442306146466>",
    "base": "<:base:1381357523369594930>",
    "solana": "<:sol:1381357455279128747>",
    "binance": "<:bnb:1381357508463165581>",
    "arbitrum": "<:arb:1381357470093676574>",
    "bitcoin": "<:btc:1381357426673979492>",
    "sui": "<:sui:1381357487462023338>"
}

async def get_token_data(ca: str) -> dict:

    dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{ca}"
    data={}
    async with aiohttp.ClientSession() as session:
        async with session.get(dex_url) as resp:
            if resp.status == 200:
                try:
                    dex_data = await resp.json()
                    if dex_data['pairs'][0]:
                        data['ca']=ca
                        data['mc'] = format_crypto_number(dex_data['pairs'][0]['fdv']) if dex_data['pairs'] else 'N/A'
                        data['vol24'] = format_crypto_number(dex_data['pairs'][0]['volume']['h24']) if dex_data['pairs'] else 'N/A'
                        data['vol1'] = format_crypto_number(dex_data['pairs'][0]['volume']['h1']) if dex_data['pairs'] else 'N/A'
                        data['chain'] = dex_data['pairs'][0]['chainId']
                        data['name'] = dex_data['pairs'][0]['baseToken']['name']
                        data['token'] = dex_data['pairs'][0]['baseToken']['symbol']
                        
                        img_url = None
                        info = dex_data['pairs'][0].get('info', {})
                        if info:
                            img_url = info.get('openGraph') or info.get('header') or info.get('imageUrl')
                        data['img'] = img_url

                        return data
                    else:
                        return None
                except Exception as e:
                    print("🔥 Error:", e)
                    return None
            else:
                return None

def format_crypto_number(value):
    try:
        value = float(value)
        if value >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"
        elif value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.2f}K"
        else:
            return f"{value:.2f}"
    except:
        return "N/A"

async def create_jeet_card(data: dict) -> Embed:
    chain_id = data['chain'].lower()
    emoji = CHAIN_EMOJIS.get(chain_id, "<:cute:1380744743415189704>")

    body = f"""
{emoji}  {data['chain'].upper()}
💹 MC: `{data['mc']}`
📈 VOL: `{data['vol24']}` 
📉 1H: `{data['vol1']}`
☎️ CALLS: `{data['calls']}`
🤙 BY: `{data['source']}`
📋 CA: `{data['ca']}`

<a:fire:1380742987843239946> **New Jeet Signal!**

💡 **Tips :**
- Ape now, regret later 😉
- **ALL CA HERE ARE SUBJECTED TO GO TO 0**
- TAKE __**PROFITS AT 2X**__ MFERR
"""

    embed = Embed(
      title=f"${data['token']}",
      url=f"https://dexscreener.com/{data['chain']}/{data['ca']}",
      description=body,
      colour=Colour.gold(),
      timestamp=datetime.now()
    )
    embed.set_author(name=f"  {data['name']}")
    
    if data['img']:
        embed.set_image(url=f"{data['img']}")
    
    embed.add_field(name="<a:letsgo:1380746421929771128>",value=f"> ```{data['ca']}```")
    
    embed.set_footer(
        text="DYOR !! PIKA.. PIKA...",
        icon_url="https://cdn3.emoji.gg/emojis/58668-pixelpikachu.gif"
    )

    return embed

async def create_TA_card(data: dict) -> Embed:
    embed = Embed(
        title=f"<a:letsgo:1380746421929771128> Signal from {data['source']}",
        description=data['raw'],
        colour=Colour.gold(),
        timestamp=datetime.now()
    )
    embed.set_footer(text="DYOR & Watch Carefully 📉📈",icon_url="https://cdn3.emoji.gg/emojis/58668-pixelpikachu.gif")
    return embed