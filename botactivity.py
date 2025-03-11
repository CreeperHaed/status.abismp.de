import discord
from discord.ext import tasks, commands
from mcstatus import JavaServer

try: import config_local as config
except ImportError: import config

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
        # print(f"Error checking server: {e}")
        return {
            "online": False,
            "players": 0,
            "protocol": 0
        }

# Task to update the bot's activity
@tasks.loop(seconds=5)
async def update_bot_activity():
    server_status = await check_minecraft_server()
    if server_status["online"]:
        if server_status['protocol'] != -1:
            name=f"{config.MC_SERVER_NAME} 🟢"
            state=f"{server_status['players']} players Online 🌍"
        else:
            name=f"{config.MC_SERVER_NAME} 🟡"
            state="Server Maintenance 🚧"
    else:
        name=f"{config.MC_SERVER_NAME} 🔴"
        state="🔻 Server Offline 🔻"

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=name,state=state))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_bot_activity.start()

bot.run(config.DISCORD_BOT_TOKEN)