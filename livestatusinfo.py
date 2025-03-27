import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer
import config

last_status = None
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

# Task to update the channel - extremely slow because of discords rate limit
@tasks.loop(seconds=300)
async def update_channel():
    global last_status
    server_status = await check_minecraft_server()
    if server_status["online"]:
        if server_status['protocol'] != -1:
            new_status="🟢 yap.abismp.de 🟢"
        else:
            new_status="🟡 yap.abismp.de 🟡"
    else:
        new_status="🔴 yap.abismp.de 🔴"

    channel = bot.get_channel(config.LIVESTATUS_CHANNEL_ID)
    if channel:
        if last_status != new_status:
            await channel.edit(name=new_status)
            last_status = new_status
        else:
            print("unmodified status")

@bot.event
async def ready():
    print(f'Logged in as {bot.user.name}')
    update_channel.start()

bot.run(config.DISCORD_BOT_TOKEN)