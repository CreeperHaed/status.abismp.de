import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)
temp_channels = {}

# Event: When a user joins or leaves a voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joined the specific voice channel
    if after.channel and after.channel.id == config.CREATEVC_CHANNEL_ID:
        # Create a new temporary voice channel
        category = bot.get_channel(config.CREATEVC_CATEGORY_ID)
        if category and isinstance(category, discord.CategoryChannel):
            new_channel = await category.create_voice_channel(
                name=f"{member.display_name}'s VC",
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
bot.run(config.DISCORD_BOT_TOKEN)