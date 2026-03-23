import discord
from discord.ext import tasks, commands
from discord import app_commands
import requests
import os
import random
import datetime
import platform

TOKEN = os.getenv("DISCORD_TOKEN")
URL_TO_CHECK = os.getenv("URL_TO_CHECK", "https://allshop.dpdns.org/")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ─── Helper ────────────────────────────────────────────────────────────────────

async def check_server_status():
    try:
        response = requests.get(URL_TO_CHECK, timeout=10)
        if response.status_code == 200:
            return "✅ Server is working!"
        else:
            return f"⚠️ Server error: {response.status_code}"
    except requests.exceptions.RequestException:
        return "❌ Server down"

# ─── Events ────────────────────────────────────────────────────────────────────

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

# ─── Status loop ───────────────────────────────────────────────────────────────

@tasks.loop(minutes=1)
async def update_status():
    try:
        status = await check_server_status()
        activity = discord.Activity(type=discord.ActivityType.watching, name=status)
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(f"Error updating status: {e}")

# ─── /checkserver ──────────────────────────────────────────────────────────────

@bot.tree.command(name="checkserver", description="Check server status")
async def checkserver(interaction: discord.Interaction):
    status = await check_server_status()
    await interaction.response.send_message(status)

# ─── /game ─────────────────────────────────────────────────────────────────────

GAMES_3DS = [
    "The Legend of Zelda: Ocarina of Time 3D",
    "Super Mario 3D Land",
    "Pokémon X",
    "Pokémon Y",
    "Pokémon Sun",
    "Pokémon Moon",
    "Pokémon Omega Ruby",
    "Pokémon Alpha Sapphire",
    "Animal Crossing: New Leaf",
    "Fire Emblem: Awakening",
    "Fire Emblem Fates",
    "Luigi's Mansion: Dark Moon",
    "Mario Kart 7",
    "Kirby: Triple Deluxe",
    "Kirby: Planet Robobot",
    "Metroid: Samus Returns",
    "Donkey Kong Country Returns 3D",
    "Kid Icarus: Uprising",
    "Star Fox 64 3D",
    "The Legend of Zelda: A Link Between Worlds",
    "The Legend of Zelda: Majora's Mask 3D",
    "Monster Hunter 4 Ultimate",
    "Monster Hunter Generations",
    "Xenoblade Chronicles 3D",
    "Bravely Default",
    "Bravely Second: End Layer",
    "Persona Q: Shadow of the Labyrinth",
    "Shin Megami Tensei IV",
    "Rune Factory 4",
    "Stardew Valley (not on 3DS, but Harvest Moon: The Lost Valley)",
    "Sonic Generations",
    "Shovel Knight",
    "Cave Story",
    "Pushmo",
    "Crashmo",
    "The Legend of Zelda: Tri Force Heroes",
    "Hyrule Warriors Legends",
    "Theatrhythm Final Fantasy",
    "Professor Layton and the Azran Legacy",
    "Ace Attorney: Dual Destinies",
]

GAME_DESCRIPTIONS = {
    "The Legend of Zelda: Ocarina of Time 3D": (
        "🗡️ **The Legend of Zelda: Ocarina of Time 3D**\n"
        "A legendary action-adventure remaster for the Nintendo 3DS. Play as young Link as he embarks "
        "on a quest through the land of Hyrule to stop the evil Gerudo king Ganondorf from obtaining "
        "the Triforce. With fully remade HD-style visuals, gyroscopic aiming, and a revamped Master "
        "Quest mode included, this is considered one of the greatest games ever made.\n"
        "🕹️ **Genre:** Action-Adventure\n⭐ **Rating:** 10/10 — A timeless classic."
    ),
    "Super Mario 3D Land": (
        "🍄 **Super Mario 3D Land**\n"
        "Mario's first proper 3D platformer on a handheld! Bowser has kidnapped Princess Peach and "
        "scattered the Super Leaves across the world. Combining elements from classic 2D Mario games "
        "with 3D gameplay, this title makes brilliant use of the 3DS's stereoscopic 3D effect. "
        "The Tanooki Suit makes a glorious return!\n"
        "🕹️ **Genre:** 3D Platformer\n⭐ **Rating:** 9/10 — Essential 3DS fun."
    ),
    "Animal Crossing: New Leaf": (
        "🏡 **Animal Crossing: New Leaf**\n"
        "Wake up — you've been elected mayor! Build your dream village, befriend quirky animal "
        "neighbors, catch bugs, fish, and decorate your home to your heart's content. With hundreds "
        "of hours of relaxing gameplay, seasonal events, and online multiplayer, this is one of the "
        "most addictive games on the 3DS. Perfect for winding down.\n"
        "🕹️ **Genre:** Life Simulation\n⭐ **Rating:** 9.5/10 — Endlessly charming."
    ),
    "Fire Emblem: Awakening": (
        "⚔️ **Fire Emblem: Awakening**\n"
        "A critically acclaimed tactical RPG that saved the Fire Emblem franchise. Lead Chrom and "
        "his Shepherds against the Risen undead and the schemes of the Grimleal cult. Features "
        "deep strategic combat, relationship-building between units (which affects stats and "
        "unlocks children units), and a gripping story with multiple endings.\n"
        "🕹️ **Genre:** Tactical RPG\n⭐ **Rating:** 9.5/10 — Genre-defining."
    ),
    "Pokémon X": (
        "🦋 **Pokémon X**\n"
        "The first mainline Pokémon game in full 3D! Explore the Kalos region, inspired by France, "
        "and discover the new Fairy type and the powerful Mega Evolution mechanic. The story touches "
        "on themes of beauty, life, and the power of bonds. Includes 720+ Pokémon and introduces "
        "some fan-favorites like Sylveon and Greninja.\n"
        "🕹️ **Genre:** RPG\n⭐ **Rating:** 8.5/10 — A beautiful new era for Pokémon."
    ),
    "Monster Hunter 4 Ultimate": (
        "🐉 **Monster Hunter 4 Ultimate**\n"
        "One of the best entries in the Monster Hunter series. Hunt over 100 massive monsters across "
        "breathtaking environments, craft gear from their parts, and master 14 different weapon types. "
        "The addition of vertical terrain, mounting mechanics, and an excellent online multiplayer "
        "mode make this an absolute must-play for fans of action RPGs.\n"
        "🕹️ **Genre:** Action RPG\n⭐ **Rating:** 9/10 — Hundreds of hours of content."
    ),
    "Kid Icarus: Uprising": (
        "😇 **Kid Icarus: Uprising**\n"
        "After a 25-year hiatus, Pit returns in this wildly creative action game. Battle through "
        "air-based rail shooting sections and intense ground combat levels. With a witty story full "
        "of humor, a robust weapon crafting system, and online multiplayer, this game packs more "
        "ideas than most full-priced console titles.\n"
        "🕹️ **Genre:** Action Shooter\n⭐ **Rating:** 9/10 — Surprisingly deep and fun."
    ),
    "Bravely Default": (
        "💎 **Bravely Default**\n"
        "A love letter to classic JRPGs with a brilliant twist: the Brave/Default combat system. "
        "Store turns for later or spend turns you haven't earned yet for powerful combos. Set in "
        "the beautifully hand-crafted world of Luxendarc, this game features stunning visuals, "
        "excellent music by Revo, and four memorable characters on an emotional journey.\n"
        "🕹️ **Genre:** JRPG\n⭐ **Rating:** 9/10 — A modern JRPG masterpiece."
    ),
}

DEFAULT_DESCRIPTION = (
    " **{title}**\n"
    "This Title isn't in the Database right now"

)

@bot.tree.command(name="game", description="Get info about a random Nintendo 3DS game")
@app_commands.describe(title="Optional: Name of a specific 3DS game (leave empty for random)")
async def game(interaction: discord.Interaction, title: str = None):
    await interaction.response.defer()

    if title:
        # Try to find a close match
        match = next((g for g in GAMES_3DS if title.lower() in g.lower()), None)
        chosen = match if match else title
    else:
        chosen = random.choice(GAMES_3DS)

    description = GAME_DESCRIPTIONS.get(
        chosen,
        DEFAULT_DESCRIPTION.format(title=chosen)
    )

    embed = discord.Embed(
        description=description,
        color=discord.Color.red()
    )
    embed.set_footer(text="Nintendo 3DS Game Info • Type /game to get another!")
    await interaction.followup.send(embed=embed)

# ─── /ping ─────────────────────────────────────────────────────────────────────

@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    if latency < 100:
        emoji = "🟢"
    elif latency < 200:
        emoji = "🟡"
    else:
        emoji = "🔴"
    await interaction.response.send_message(f"{emoji} Pong! Latency: **{latency}ms**")

# ─── /uptime ───────────────────────────────────────────────────────────────────

bot.start_time = datetime.datetime.utcnow()

@bot.tree.command(name="uptime", description="Show how long the bot has been running")
async def uptime(interaction: discord.Interaction):
    delta = datetime.datetime.utcnow() - bot.start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days = delta.days
    parts = []
    if days: parts.append(f"**{days}d**")
    if hours: parts.append(f"**{hours}h**")
    if minutes: parts.append(f"**{minutes}m**")
    parts.append(f"**{seconds}s**")
    await interaction.response.send_message(f" Bot has been online for: {' '.join(parts)}")

# ─── /roll ─────────────────────────────────────────────────────────────────────

@bot.tree.command(name="roll", description="Roll a dice (e.g. d6, d20, d100)")
@app_commands.describe(dice="Dice type: d4, d6, d8, d10, d12, d20, d100")
@app_commands.choices(dice=[
    app_commands.Choice(name="d4",  value=4),
    app_commands.Choice(name="d6",  value=6),
    app_commands.Choice(name="d8",  value=8),
    app_commands.Choice(name="d10", value=10),
    app_commands.Choice(name="d12", value=12),
    app_commands.Choice(name="d20", value=20),
    app_commands.Choice(name="d100",value=100),
])
async def roll(interaction: discord.Interaction, dice: int = 6):
    result = random.randint(1, dice)
    if result == dice:
        msg = f"🎲 You rolled a **d{dice}** and got: **{result}** 🎉 *Critical hit!*"
    elif result == 1:
        msg = f"🎲 You rolled a **d{dice}** and got: **{result}** 💀 *Critical fail!*"
    else:
        msg = f"🎲 You rolled a **d{dice}** and got: **{result}**"
    await interaction.response.send_message(msg)

# ─── /coinflip ─────────────────────────────────────────────────────────────────

@bot.tree.command(name="coinflip", description="Flip a coin — heads or tails?")
async def coinflip(interaction: discord.Interaction):
    result = random.choice(["Heads", "Tails"])
    emoji = "🪙" if result == "Heads" else "🪙"
    await interaction.response.send_message(f"{emoji} **{result}!**")

# ─── /8ball ────────────────────────────────────────────────────────────────────

EIGHT_BALL_RESPONSES = [
    "✅ It is certain.", "✅ It is decidedly so.", "✅ Without a doubt.",
    "✅ Yes, definitely.", "✅ You may rely on it.", "✅ As I see it, yes.",
    "✅ Most likely.", "✅ Probably.", "✅ Yes.", "✅ Signs point to yes.",
    "🤷 Reply hazy, try again.", "🤷 Ask again later.",
    "🤷 Better not tell you now.", "🤷 Cannot predict now.",
    "🤷 Concentrate and ask again.",
    "❌ Don't count on it.", "❌ definitely not!!", "❌ My sources say no.",
    "❌ definitely not!!", "❌ Very doubtful.",
]

@bot.tree.command(name="8ball", description="Ask the Magic 8-Ball a yes/no question")
@app_commands.describe(question="Your yes/no question")
async def eight_ball(interaction: discord.Interaction, question: str):
    answer = random.choice(EIGHT_BALL_RESPONSES)
    embed = discord.Embed(color=discord.Color.dark_purple())
    embed.add_field(name="🎱 Question", value=question, inline=False)
    embed.add_field(name="Answer", value=answer, inline=False)
    await interaction.response.send_message(embed=embed)

# ─── /serverinfo ───────────────────────────────────────────────────────────────

@bot.tree.command(name="serverinfo", description="Show info about this server")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("❌ This command must be used in a server.")
        return

    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.blue())
    embed.add_field(name="Owner",    value=str(guild.owner),          inline=True)
    embed.add_field(name="Members",  value=str(guild.member_count),   inline=True)
    embed.add_field(name="Channels", value=str(len(guild.channels)),  inline=True)
    embed.add_field(name="Roles",    value=str(len(guild.roles)),     inline=True)
    embed.add_field(name="Boosts",   value=str(guild.premium_subscription_count), inline=True)
    embed.add_field(name="Created",  value=guild.created_at.strftime("%d.%m.%Y"), inline=True)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    await interaction.response.send_message(embed=embed)

# ─── /userinfo ─────────────────────────────────────────────────────────────────

@bot.tree.command(name="userinfo", description="Show info about a user")
@app_commands.describe(member="The user to look up (leave empty for yourself)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"👤 {target.display_name}", color=target.color)
    embed.add_field(name="Username",  value=str(target),                          inline=True)
    embed.add_field(name="ID",        value=str(target.id),                       inline=True)
    embed.add_field(name="Bot?",      value="Yes" if target.bot else "No",        inline=True)
    embed.add_field(name="Joined server",
                    value=target.joined_at.strftime("%d.%m.%Y") if hasattr(target, "joined_at") and target.joined_at else "N/A",
                    inline=True)
    embed.add_field(name="Account created",
                    value=target.created_at.strftime("%d.%m.%Y"),
                    inline=True)
    top_role = target.top_role.name if hasattr(target, "top_role") else "N/A"
    embed.add_field(name="Top role", value=top_role, inline=True)
    embed.set_thumbnail(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# ─── /botinfo ──────────────────────────────────────────────────────────────────

@bot.tree.command(name="botinfo", description="Show information about this bot")
async def botinfo(interaction: discord.Interaction):
    embed = discord.Embed(title="🤖 Bot Info", color=discord.Color.green())
    embed.add_field(name="Bot Name",     value=str(bot.user),              inline=True)
    embed.add_field(name="Servers",      value=str(len(bot.guilds)),        inline=True)
    embed.add_field(name="Latency",      value=f"{round(bot.latency*1000)}ms", inline=True)
    embed.add_field(name="Python",       value=platform.python_version(),   inline=True)
    embed.add_field(name="discord.py",   value=discord.__version__,         inline=True)
    embed.add_field(name="Monitoring",   value=URL_TO_CHECK,                inline=False)
    embed.set_footer(text="Use /checkserver to check the monitored server status.")
    await interaction.response.send_message(embed=embed)

# ─── Run ───────────────────────────────────────────────────────────────────────

bot.run(TOKEN)
