"""
Yeye its the chatbot - yes I would be keen on integrating the bot on both my servers. 
I would say look into the price of o1 mini tokens and see viability/results.

In terms of bot implementation itself, what you have is a good start but here is perhaps how it could be implemented in discord format (just throwing ideas)

Bot should be like meangpt - in a designated channel it responds to every message or if directly tagged or replied itself outside of designated channel it responds. User has access to /change command or /menu or smth which opens up an embedded with buttons.

In the embed you can have like 4 buttons- analyst diplomat etc, and upon pressing quadra selection  it gives you the 4 types to press and then the model name (M/F).

I’m guessing the bot’ll have to remember the user’s last selected model and keep it user specific.


should the bot have a standard personality?

- make bot respond directly in dedicated channel
- make bot 

"""

# This example requires the 'message_content' intent.
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Define your designated channel ID (replace with your actual channel ID)
    DESIGNATED_CHANNEL_ID = 1329310835994136609  # You'll need to get this from Discord

    try:
        # Case 1: In designated channel - respond to everything
        if message.channel.id == DESIGNATED_CHANNEL_ID:
            await message.channel.send('I respond to everything here!')
            
        # Case 2: Outside designated channel - only respond if:
        else:
            # 2a: Bot is mentioned
            if bot.user in message.mentions:
                await message.channel.send('You mentioned me!')
                
            # 2b: Message is a reply to the bot
            elif message.reference and message.reference.resolved.author == bot.user:
                await message.channel.send('You replied to me!')

    except discord.errors.Forbidden:
        print(f"Missing permissions in channel: {message.channel.name}")

class PersonalityButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Analyst", style=discord.ButtonStyle.primary)
    async def analyst_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You selected Analyst!", ephemeral=True)
        
    @discord.ui.button(label="Diplomat", style=discord.ButtonStyle.success)
    async def diplomat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You selected Diplomat!", ephemeral=True)
        
    @discord.ui.button(label="Sentinel", style=discord.ButtonStyle.danger)
    async def sentinel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You selected Sentinel!", ephemeral=True)
        
    @discord.ui.button(label="Explorer", style=discord.ButtonStyle.secondary)
    async def explorer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("You selected Explorer!", ephemeral=True)

@bot.tree.command(name="menu", description="Open personality selection menu")
async def menu(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Choose Your Bot Personality",
        description="Select one of the following personalities:",
        color=discord.Color.blue()
    )
    embed.add_field(name="Available Types", value="🧠 Analyst\n🤝 Diplomat\n⚔️ Sentinel\n🌟 Explorer")
    
    view = PersonalityButtons()
    await interaction.response.send_message(embed=embed, view=view)

bot.run(os.getenv('DISCORD_TOKEN'))
