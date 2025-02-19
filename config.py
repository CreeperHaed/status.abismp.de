try:
    from config_local import *
except ImportError:
    # Replace the placeholder values with your own data
    DISCORD_BOT_TOKEN = "your_discord_bot_token_here"

    LIVESTATUS_CHANNEL_ID = 123456789012345678
    CREATEVC_CHANNEL_ID = 123456789012345679
    CREATEVC_CATEGORY_ID = 123456789012345680

    MC_SERVER_IP = "your.server.ip"
    MC_SERVER_PORT = 25565  # Default Minecraft port (change if needed)

    # Here are some examples of what else could be monitored on the Server
    MC_VOICECHAT_PORT = 24456

# List of services to monitor
ports = [  # supported types: "minecraft", tcp, udp, http, https
    {
        "name": "Minecraft Server",
        "host": MC_SERVER_IP,
        "port": MC_SERVER_PORT,
        "type": "minecraft"
    },
    {
        "name": "Minecraft Voicechat",
        "host": MC_SERVER_IP,
        "port": MC_VOICECHAT_PORT,
        "type": "udp"
    },
    {
        "name": "Website",
        "host": MC_SERVER_IP,
        "port": 80,
        "type": "http"
    }
]