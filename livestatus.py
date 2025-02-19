import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Minecraft server details
MC_SERVER_IP = "your.minecraft.server.ip"  # Replace with your server IP
MC_SERVER_PORT = 25565  # Default Minecraft port (change if needed)
CHANNEL_ID = 1234567890123456789  # your channel ID here (text-based channels do not support spaces)

# Function to check Minecraft server status
async def check_minecraft_server():
    try:
        server = JavaServer.lookup(f"{MC_SERVER_IP}:{MC_SERVER_PORT}")
        status = server.status()
        return {
            "online": True,
            "players": status.players.online,
            "max_players": status.players.max,
            "protocol": status.version.protocol,
            "latency": status.latency
        }
    except Exception as e:
        print(f"Error checking server: {e}")
        return {
            "online": False,
            "players": 0,
            "max_players": 0,
            "protocol": 0,
            "latency": 0
        }

# Task to update the channel
@tasks.loop(seconds=30)
async def update_channel():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        server_status = await check_minecraft_server()
        if server_status["online"]:
            if server_status['protocol'] != -1:
                await channel.edit(name=f"Server: 🟢 {server_status['players']}")
            else:
                await channel.edit(name=f"Server: 🟡🚧")
        else:
            await channel.edit(name="Server: 🔴 OFFLINE")

# Bot startup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_channel.start()

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')