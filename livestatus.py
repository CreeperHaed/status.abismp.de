import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer
import config

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to check Minecraft server status
async def check_minecraft_server():
    try:
        server = JavaServer.lookup(f"{config.MC_SERVER_IP}:{config.MC_SERVER_PORT}")
        status = server.status()
        return {
            "online": True,
            "players": status.players.online,
            "protocol": status.version.protocol
        }
    except Exception as e:
        print(f"Error checking server: {e}")
        return {
            "online": False,
            "players": 0,
            "protocol": 0
        }

# Task to update the channel
@tasks.loop(seconds=30)
async def update_channel():
    channel = bot.get_channel(config.LIVESTATUS_CHANNEL_ID)
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

bot.run(config.DISCORD_BOT_TOKEN)