import discord
from discord.ext import tasks
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")  # ← Kommt von Railway, nicht aus dem Code
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
URL_TO_CHECK = os.getenv("URL_TO_CHECK", "https://allshop.dpdns.org/")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user}')
    check_website.start()

@tasks.loop(minutes=5)
async def check_website():
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        if response.status_code == 200:
            status = "Server is working!"
        else:
            status = f"Server works but gets this error: {response.status_code}"
    except requests.exceptions.RequestException:
        status = "Server down"
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(status)

client.run(TOKEN)
