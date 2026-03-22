import discord
from discord.ext import tasks, commands
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
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
            return f"⚠️ Server error: {response.status_code}"
    except requests.exceptions.RequestException:
        return "❌ Server down"

@bot.event
async def on_ready():
    print(f'{bot.user} is online')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    
    if not update_status.is_running():
        update_status.start()

@tasks.loop(minutes=1)
async def update_status():
    try:
        status = await check_server_status()
        activity = discord.Activity(type=discord.ActivityType.watching, name=status)
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(f"Error updating status: {e}")

@bot.tree.command(name="checkserver", description="Check server status")
async def checkserver(interaction: discord.Interaction):
    await interaction.response.defer()
    status = await check_server_status()
    await interaction.followup.send(status)

bot.run(TOKEN)
