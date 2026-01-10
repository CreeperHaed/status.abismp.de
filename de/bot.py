###################  C O N F I G  ###################

PUBLIC_ADDRESS = "abismp.de"
LOCAL_ADDRESS = "localhost"
PORT = 25566

STATUS_CHANNEL_ID = 1304583837841358889
JOIN_CHANNEL_ID = 1257342073464422415
VC_CATEGORY_ID = 1257340215882678432

TICKET_CATEGORY_ID = 1300085191632486440
LOG_CHANNEL_ID = 1300085197014040586
TRANSCRIPT_FOLDER = "transcripts"

STAFF_ROLE_ID = 1257336634412892264
HOSTER_ROLE_ID = 1257338391398191157
OWNER_ID = 825736363814289448
OWNER_NAME = "creeperhaed"

ROLES = {
    "Java": ("💻", 1318600244157616168),
    "Bedrock": ("🎮", 1304010014968774656)
}

BOT_TOKEN = ""

##############  T R A N S L A T I O N  ##############

ticket_embed_title = "Ticket erstellen!"
click_the_button_below_to_create_a_ticket = "Klick die Schaltfläche unten um ein Ticket zu erstellen!"
create_ticket = "Erstelle ein Ticket"

how_can_we_help_you = "Wie können wir dir helfen?:"
choose_category = "Wähle eine Kategorie..."

TICKET_TYPE = {
    "help": "Hilfe",
    "help_emoji": "🔧",
    "question": "Frage",
    "question_emoji": "❔",
    "report": "Meldung",
    "report_emoji": "🚫"
}

creating_ticket = "⏳ Dein Ticket wird erstellt..."
ticket_created = "✅ Ticket erstellt: {channel}"

greeting = "Grüß dich {user}! Unsere Mods werden dir in Kürze weiterhelfen."
call_staff = "Moderation rufen"
close_ticket = "Ticket schließen"
calls_staff = "🔔 {user} ruft <@&{staff_id}>!"

ticket_repaired = "🔧 Ticket repariert"
buttons_refreshed = "Die Buttons wurden aktualisiert!"
deleted_files_and_folders = "🧹 Deleted {deleted_files} test file{s1} and {deleted_folders} empty folder{s2}."

self_asignable_roles = "📋 Auswählbare Rollen"
click_a_button_below_to_change_a_role = "Klicke eines der Schaltflächen um eine Rolle zu ändern!"
role_added = "**{role}** wurde hinzugefügt! ✅"
role_removed = "**{role}** wurde entfernt! ✅"

######################  L O G  ######################

LOG_EMBED = {
    "title_opened": "Neues Ticket erstellt",
    "title_closed": "Ticket geschlossen",
    "ticket": "Ticket",
    "type": "Typ",
    "creator": "Ersteller",
    "created_by": "Erstellt von",
    "closed_by": "Geschlossen von",
    "no_transcript": "Geschlossen ohne Transcript!"
}
TRANSCRIPT = {
    "created_for": "📝 Transkript für {user}",
    "created_by": "(Erstellt von {creator})",
    "creator_left": "(⚠️ Ersteller nicht auf dem Server ⚠️)"
}
ERRORS = {
    "can_only_be_closed_by": "❌ Nur der Ticket-Ersteller oder Moderatoren können das Ticket schließen!",
    "only_creator_can_call": "❌ Nur der Ticket-Ersteller kann Mods rufen!",
    "command_only_in_tickets": "❌ Dieser Befehl funktioniert nur in Tickets!",
    "only_owner_can_do_that": f"❌ Nur {OWNER_NAME} kann das!",
    "this_role_was_not_found": "❌ Die Rolle wurde nicht gefunden!"
}

###################  D E S I G N  ###################

STATUS_TABLE = {
    'online': {
        "channel_status": f"🟢 {PUBLIC_ADDRESS} 🟢",
        "name": "{players} Spieler Online 🌍",
        "status": "online"
    },
    'maintenance': {
        "channel_status": f"🟡 {PUBLIC_ADDRESS} 🟡",
        "name": "🚧 Server Maintenance 🚧",
        "status": "online"
    },
    'unreachable': {
        "channel_status": f"🟠 {PUBLIC_ADDRESS} 🟠",
        "name": "⚠️ Server Unreachable ⚠️",
        "status": "idle"
    },
    'offline': {
        "channel_status": f"🔴 {PUBLIC_ADDRESS} 🔴",
        "name": "🔻 Server Offline 🔻",
        "status": "idle"
    }
}

TICKET_EMBED_IMAGE_URL = "https://i.imgur.com/FoI5ITb.png"
TICKET_EMBED_COLOR = 0xfcd005
EMBED_COLOR_OPENED = 0x2ecc71
EMBED_COLOR_CLOSED = 0xe74c3c

#####################################################

import discord
from discord.ext import tasks, commands
from discord.ui import Button, View, Select
from mcstatus import JavaServer
import os
import datetime
import html

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)
last_status = None
temp_channels = {}

os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

async def check_minecraft_server():
    try:
        server = JavaServer.lookup(f"{PUBLIC_ADDRESS}:{PORT}")
        status = server.status()
        return {
            "online": True, "running": True,
            "players": status.players.online,
            "protocol": status.version.protocol,
            "motd": status.description
        }
    except Exception:
        try:
            server = JavaServer.lookup(f"{LOCAL_ADDRESS}:{PORT}")
            status = server.status()
            return {
                "online": False, "running": True,
                "players": 0,
                "protocol": None, "motd": None
            }
        except Exception:
            return {
                "online": False, "running": False,
                "players": 0,
                "protocol": None, "motd": None
            }

async def check_ticket(channel: discord.TextChannel, creator_id):
    async for msg in channel.history(limit=None, oldest_first=True):
        if msg.author.id == creator_id: 
            return ""
    return f"\n-# {LOG_EMBED["no_transcript"]}"

async def generate_transcript(channel: discord.TextChannel, creator):
    today = datetime.datetime.now().strftime("%Y-%m")
    dated_folder = f"{TRANSCRIPT_FOLDER}/{today}"
    os.makedirs(dated_folder, exist_ok=True)
    
    transcript_filename = f"{dated_folder}/{creator if creator != None else channel.name.removeprefix("❔-").removeprefix("🔧-").removeprefix("🚫-").removesuffix("-ticket")}-{datetime.datetime.now().strftime('%d-%H%M%S')}.html"
    
    with open(transcript_filename, "w", encoding="utf-8") as f:
        f.write(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Transcript of {channel.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .message {{ margin-bottom: 15px; }}
                .author {{ font-weight: bold; color: #7289da; }}
                .timestamp {{ color: #747f8d; font-size: 0.8em; }}
                .content {{ margin-left: 10px; }}
            </style>
        </head>
        <body>
            <h1>Transcript of {channel.name}</h1>
            <h3>Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h3>
            <div class="messages">
        """)

        async for message in channel.history(limit=None, oldest_first=True):
            if message.author != bot.user:
                f.write(f"""
                <div class="message">
                    <span class="author">{html.escape(message.author.display_name)}</span>
                    <span class="timestamp">{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</span>
                    <div class="content">{html.escape(message.content)}</div>
                </div>
                """)

        f.write("""
            </div>
        </body>
        </html>
        """)
    
    return transcript_filename

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label=create_ticket, style=discord.ButtonStyle.success, emoji="🔧", custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        dropdown = Select(
            placeholder=choose_category,
            options=[
                discord.SelectOption(label=TICKET_TYPE["question"], value="question", emoji=TICKET_TYPE["question_emoji"]),
                discord.SelectOption(label=TICKET_TYPE["help"], value="help", emoji=TICKET_TYPE["help_emoji"]),
                discord.SelectOption(label=TICKET_TYPE["report"], value="report", emoji=TICKET_TYPE["report_emoji"]),
            ]
        )

        async def dropdown_callback(interaction: discord.Interaction):
            ticket_type = dropdown.values[0]
            guild = interaction.guild
            category = guild.get_channel(TICKET_CATEGORY_ID)
            staff_role = guild.get_role(STAFF_ROLE_ID)

            await interaction.response.edit_message(content=creating_ticket, view=None)

            emoji = TICKET_TYPE[ticket_type+"_emoji"]
            channel = await guild.create_text_channel(
                name=f"{emoji}-{interaction.user.name}s-ticket",
                topic=str(interaction.user.id),
                category=category
            )

            await channel.set_permissions(guild.default_role, view_channel=False)
            await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)
            await channel.set_permissions(staff_role, view_channel=True, send_messages=True, manage_messages=True)

            embed = discord.Embed(
                title=f"{TICKET_TYPE[ticket_type]}-Ticket",
                description=greeting.format(user=interaction.user.mention),
                color=TICKET_EMBED_COLOR
            )

            await channel.send(embed=embed, view=CloseTicketView())
            
            if log_channel := guild.get_channel(LOG_CHANNEL_ID):
                embed = discord.Embed(
                    title= LOG_EMBED["title_opened"],
                    description=(
                        f"**{LOG_EMBED["ticket"]}:** {channel.mention}\n"
                        f"**{LOG_EMBED["created_by"]}:** {interaction.user.mention}\n"
                        f"**{LOG_EMBED["type"]}:** {TICKET_TYPE[ticket_type]}"
                    ),
                    color=EMBED_COLOR_OPENED,
                    timestamp=datetime.datetime.now()
                )
                await log_channel.send(embed=embed)

            await interaction.edit_original_response(content=ticket_created.format(channel=channel.mention), view=None)

        dropdown.callback = dropdown_callback
        await interaction.response.send_message(how_can_we_help_you, view=View().add_item(dropdown), ephemeral=True)

class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
        
        close_button = Button(
            label=close_ticket,
            style=discord.ButtonStyle.danger,
            emoji="🔒",
            custom_id="close_ticket"
        )
        close_button.callback = self.close_callback
        self.add_item(close_button)
        
        call_staff_button = Button(
            label=call_staff,
            style=discord.ButtonStyle.primary,
            emoji="🔔",
            custom_id="call_staff"
        )
        call_staff_button.callback = self.call_staff_callback
        self.add_item(call_staff_button)
    
    async def close_callback(self, interaction: discord.Interaction):
        creator_id = int(interaction.channel.topic)
        is_staff = interaction.user.get_role(STAFF_ROLE_ID) is not None
        is_creator = interaction.user.id == creator_id

        if not (is_staff or is_creator):
            return await interaction.response.send_message(ERRORS["can_only_be_closed_by"],ephemeral=True)

        await interaction.response.defer()

        log_channel = interaction.guild.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            ticket_info = await check_ticket(interaction.channel, creator_id)
            if ticket_info == "":
                creator = interaction.guild.get_member(creator_id)
                transcript_file = await generate_transcript(interaction.channel, creator)
                if creator:
                    await log_channel.send(
                        f"{TRANSCRIPT["created_for"].format(user=interaction.channel.name)} {TRANSCRIPT["created_by"].format(creator=creator.display_name)}",
                        file=discord.File(open(transcript_file, "rb"))
                    )
                else:
                    await log_channel.send(
                        f"{TRANSCRIPT["created_for"].format(user=interaction.channel.name)} {TRANSCRIPT["creator_left"]}",
                        file=discord.File(open(transcript_file, "rb"))
                    )
            
            embed = discord.Embed(
                title= LOG_EMBED["title_closed"],
                description=(
                    f"**{LOG_EMBED["ticket"]}:** {interaction.channel.name}\n"
                    f"**{LOG_EMBED["creator"]}:** <@{creator_id}>\n"
                    f"**{LOG_EMBED["closed_by"]}:** {interaction.user.mention}{ticket_info}"
                ),
                color=EMBED_COLOR_CLOSED,
                timestamp=datetime.datetime.now()
            )
            await log_channel.send(embed=embed)
        
        await interaction.channel.delete()
    
    async def call_staff_callback(self, interaction: discord.Interaction):
        creator_id = int(interaction.channel.topic)
        if interaction.user.id != creator_id:
            return await interaction.response.send_message(ERRORS["only_creator_can_call"],ephemeral=True)

        await interaction.response.send_message(
            calls_staff.format(user=interaction.user.mention,staff_id=STAFF_ROLE_ID),
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

class RoleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for label, (emoji, role_id) in ROLES.items():
            self.add_item(RoleButton(label=label, emoji=emoji, role_id=role_id))

class RoleButton(discord.ui.Button):
    def __init__(self, label, emoji, role_id):
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=label,
            emoji=emoji,
            custom_id=f"role_{role_id}"
        )
        self.role_id = role_id
        
    async def callback(self, interaction: discord.Interaction):
        role = interaction.guild.get_role(self.role_id)
        if not role:
            return await interaction.response.send_message(ERRORS["this_role_was_not_found"], ephemeral=True)
            
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(role_removed.format(role=role.name), ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(role_added.format(role=role.name), ephemeral=True)

@tasks.loop(seconds=5)
async def update_bot_activity():
    global new_status
    server_status = await check_minecraft_server()
    if server_status["online"]:
        if server_status["protocol"] == -1 or "maintenance" in server_status["motd"]: discord_status = STATUS_TABLE["maintenance"]
        else: discord_status = STATUS_TABLE["online"]
    else:
        if server_status["running"]: discord_status = STATUS_TABLE["unreachable"]
        else: discord_status = STATUS_TABLE["offline"]

    new_status = discord_status["channel_status"]
    await bot.change_presence(activity=discord.CustomActivity(name=discord_status["name"].format(players=server_status["players"])),status=discord.Status[discord_status["status"]])

@tasks.loop(seconds=30)
async def update_channel():
    global last_status
    channel = bot.get_channel(STATUS_CHANNEL_ID)
    if channel:
        try:
            if last_status == new_status:
                if new_status != bot.get_channel(STATUS_CHANNEL_ID).name:
                    await channel.edit(name=new_status)
            else:
                await channel.edit(name=new_status)
                last_status = new_status
        except NameError: pass

@bot.command()
@commands.has_role(HOSTER_ROLE_ID)
async def ticket(ctx):
    embed = discord.Embed(
        title=ticket_embed_title,
        description=click_the_button_below_to_create_a_ticket,
        color=TICKET_EMBED_COLOR
    )
    embed.set_image(url=TICKET_EMBED_IMAGE_URL)
    await ctx.send(embed=embed, view=TicketView())
    await ctx.message.delete()

@bot.command()
@commands.has_role(HOSTER_ROLE_ID)
async def roles(ctx):
    embed = discord.Embed(
        title=self_asignable_roles,
        description=click_a_button_below_to_change_a_role,
        color=discord.Color.green() 
    )
    await ctx.send(embed=embed, view=RoleView())
    await ctx.message.delete()

@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def fixticket(ctx):
    if ctx.channel.category_id != TICKET_CATEGORY_ID or ctx.channel.category_id == LOG_CHANNEL_ID:
        return await ctx.send(ERRORS["command_only_in_tickets"], ephemeral=True)
    
    try: int(ctx.channel.topic) 
    except: return await ctx.send(ERRORS["command_only_in_tickets"], ephemeral=True)
   
    async for msg in ctx.channel.history(limit=10):
        if msg.components:
            await msg.delete()
    
    embed = discord.Embed(
        title=ticket_repaired,
        description=buttons_refreshed,
        color=TICKET_EMBED_COLOR
    )
    await ctx.send(embed=embed, view=CloseTicketView())
    await ctx.message.delete()

@bot.command()
@commands.has_role(STAFF_ROLE_ID)
async def silentclose(ctx):
    if ctx.channel.category_id != TICKET_CATEGORY_ID or ctx.channel.category_id == LOG_CHANNEL_ID:
        return await ctx.send(ERRORS["command_only_in_tickets"], ephemeral=True)
    
    try: int(ctx.channel.topic) 
    except: return await ctx.send(ERRORS["command_only_in_tickets"], ephemeral=True)
   
    log_channel = ctx.guild.get_channel(LOG_CHANNEL_ID)
    if log_channel:
        embed = discord.Embed(
            title= LOG_EMBED["title_closed"],
            description=(
                f"**{LOG_EMBED["ticket"]}:** {ctx.channel.name}\n"
                f"**{LOG_EMBED["creator"]}:** <@{int(ctx.channel.topic)}>\n"
                f"**{LOG_EMBED["closed_by"]}:** {ctx.author.mention}\n"
                f"-# {LOG_EMBED["no_transcript"]}"
            ),
            color=EMBED_COLOR_CLOSED,
            timestamp=datetime.datetime.now()
        )
        await log_channel.send(embed=embed)
    await ctx.channel.delete()

@bot.command()
@commands.has_role(HOSTER_ROLE_ID)
async def cleartests(ctx):
    if ctx.author.name != OWNER_NAME or ctx.author.id != OWNER_ID:
        return await ctx.send(ERRORS["only_owner_can_do_that"], ephemeral=True)
    
    deleted_files = 0
    deleted_folders = 0

    for root, _, files in os.walk(TRANSCRIPT_FOLDER, topdown=False):
        for file in files:
            if OWNER_NAME in file:
                os.remove(os.path.join(root, file))
                deleted_files += 1
        
        if not os.listdir(root):
            os.rmdir(root)
            deleted_folders += 1

    await ctx.send(
        deleted_files_and_folders.format(
            deleted_files=deleted_files,
            deleted_folders=deleted_folders,
            s1= "" if deleted_files == 1 else "s",
            s2= "" if deleted_folders == 1 else "s"
        ),
        ephemeral=True
    )

@bot.event
async def on_ready():
    bot.add_view(TicketView())
    bot.add_view(RoleView())
    bot.add_view(CloseTicketView())
    update_bot_activity.start()
    update_channel.start()

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == JOIN_CHANNEL_ID:
        category = bot.get_channel(VC_CATEGORY_ID)
        if category and isinstance(category, discord.CategoryChannel):
            new_channel = await category.create_voice_channel(
                name=f"{member.display_name}'s VC",
                user_limit=0
            )
            await member.move_to(new_channel)
            await new_channel.set_permissions(member, manage_channels=True)
            temp_channels[new_channel.id] = new_channel

    if before.channel and before.channel.id in temp_channels:
        channel = bot.get_channel(before.channel.id)
        if channel is None:
            del temp_channels[before.channel.id]
        else:
            if len(before.channel.members) == 0:
                await before.channel.delete()
                del temp_channels[before.channel.id]

@bot.tree.error
async def on_app_command_error(i, _): pass

bot.run(BOT_TOKEN)
