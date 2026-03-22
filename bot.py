import discord
from discord.ext import tasks, commands
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID_STR = os.getenv("CHANNEL_ID", "0")
CHANNEL_ID = int(CHANNEL_ID_STR) if CHANNEL_ID_STR else 0
URL_TO_CHECK = os.getenv("URL_TO_CHECK", "https://allshop.dpdns.org/")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def check_server_status():
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        if response.status_code == 200:
            return "✅ Server is working!"
        else:
            return f"⚠️ Server works but gets this error: {response.status_code}"
    except requests.exceptions.RequestException:
        return "❌ Server down"

@bot.event
async def on_ready():
    print(f'{bot.user}')
    check_website.start()
    await bot.tree.sync()

@tasks.loop(minutes=5)
async def check_website():
    if CHANNEL_ID == 0:
        print("CHANNEL_ID not set, skipping check")
        return
    status = await check_server_status()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(status)

@bot.tree.command(name="checkserver", description="Check server status")
async def checkserver(interaction: discord.Interaction):
    status = await check_server_status()
    await interaction.response.send_message(status)

bot.run(TOKEN)
