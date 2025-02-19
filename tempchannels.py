import discord
from discord.ext import commands

# Bot setup
intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
CREATE_CHANNEL_ID = 0  # your ID of the voice channel that triggers creation
CATEGORY_ID = 0  # your ID of the category where temporary channels will be created

# Dictionary to track temporary channels
temp_channels = {}

# Event: When a user joins or leaves a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined the specific voice channel
    if after.channel and after.channel.id == CREATE_CHANNEL_ID:
        # Create a new temporary voice channel
        category = bot.get_channel(CATEGORY_ID)
        if category and isinstance(category, discord.CategoryChannel):
            new_channel = await category.create_voice_channel(
                name=f"{member.name}'s Channel",
                user_limit=0  # Optional: Set a user limit
            )
            # Move the user to the new channel
            await member.move_to(new_channel)
            # Store the channel in the dictionary
            temp_channels[new_channel.id] = new_channel

    # Check if the user left a temporary voice channel
    if before.channel and before.channel.id in temp_channels:
        # Check if the channel is empty
        if len(before.channel.members) == 0:
            # Delete the channel
            await before.channel.delete()
            # Remove the channel from the dictionary
            del temp_channels[before.channel.id]

# Run the bot
bot.run('YOUR_DISCORD_BOT_TOKEN')