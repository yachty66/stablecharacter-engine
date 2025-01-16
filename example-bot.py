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

- if the user does not have a personality set i want to send him the embedd too - 
- if the user has set some personality i want to have him continue the chat with the personality 
- if the user had more then 10 messages i want him to display a prompt that he should go to the website
"""
# This example requires the 'message_content' intent.
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from llm import call_llm  # Import your LLM function

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="$", intents=intents)

user_personalities = {}
conversation_history = {}  # Store message history per user

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

    DESIGNATED_CHANNEL_ID = 1329310835994136609

    try:
        # Check if user has a personality set
        if message.author.id not in user_personalities:
            embed = discord.Embed(
                title="Choose Your Bot Personality",
                description="Please select a personality for our interaction:",
                color=discord.Color.blue()
            )
            embed.add_field(name="Available Types", value="🧠 Analyst\n🤝 Diplomat\n⚔️ Sentinel\n🌟 Explorer")
            view = PersonalityButtons()
            await message.channel.send(f"Hello {message.author.mention}! Please select a personality first:", embed=embed, view=view)
            return

        # Initialize conversation history for new users
        if message.author.id not in conversation_history:
            conversation_history[message.author.id] = []

        # Get user's selected personality
        personality = user_personalities[message.author.id]
        personality_type, gender = personality.split('-')

        # Prepare system message based on personality
        system_message = {"role": "system", "content": f"You are a {gender.lower()} {personality_type} from the 16 personalities test. Respond accordingly to maintain character consistency."}

        # Add user's new message to history
        conversation_history[message.author.id].append({"role": "user", "content": message.content})

        # Prepare messages for LLM
        messages = [system_message] + conversation_history[message.author.id][-10:]  # Keep last 10 messages

        # Check if we should respond
        should_respond = (
            message.channel.id == DESIGNATED_CHANNEL_ID or
            bot.user in message.mentions or
            (message.reference and message.reference.resolved.author == bot.user)
        )

        if should_respond:
            async with message.channel.typing():  # Show typing indicator
                # Get response from LLM
                response = call_llm(messages=messages)
                response_content = response.choices[0].message.content

                # Add assistant's response to history
                conversation_history[message.author.id].append({"role": "assistant", "content": response_content})

                # Send response
                await message.channel.send(response_content)

    except discord.errors.Forbidden:
        print(f"Missing permissions in channel: {message.channel.name}")
    except Exception as e:
        print(f"Error processing message: {e}")

class GenderButtons(discord.ui.View):
    def __init__(self, personality_type: str):
        super().__init__()
        self.personality_type = personality_type
        
    @discord.ui.button(label="Male", style=discord.ButtonStyle.primary)
    async def male_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_personalities[interaction.user.id] = f"{self.personality_type}-M"
        conversation_history[interaction.user.id] = []  # Initialize empty history
        await interaction.response.send_message(
            f"You've selected a Male {self.personality_type} personality!", 
            ephemeral=True
        )
        
    @discord.ui.button(label="Female", style=discord.ButtonStyle.secondary)
    async def female_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_personalities[interaction.user.id] = f"{self.personality_type}-F"
        conversation_history[interaction.user.id] = []  # Initialize empty history
        await interaction.response.send_message(
            f"You've selected a Female {self.personality_type} personality!", 
            ephemeral=True
        )

class AnalystButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="INTJ", style=discord.ButtonStyle.primary)
    async def intj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your INTJ personality:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("INTJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="INTP", style=discord.ButtonStyle.primary)
    async def intp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your INTP personality:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("INTP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ENTJ", style=discord.ButtonStyle.primary)
    async def entj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ENTJ personality:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ENTJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ENTP", style=discord.ButtonStyle.primary)
    async def entp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ENTP personality:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ENTP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class DiplomatButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="INFJ", style=discord.ButtonStyle.success)
    async def infj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your INFJ personality:",
            color=discord.Color.green()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("INFJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="INFP", style=discord.ButtonStyle.success)
    async def infp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your INFP personality:",
            color=discord.Color.green()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("INFP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ENFJ", style=discord.ButtonStyle.success)
    async def enfj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ENFJ personality:",
            color=discord.Color.green()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ENFJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ENFP", style=discord.ButtonStyle.success)
    async def enfp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ENFP personality:",
            color=discord.Color.green()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ENFP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class SentinelButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="ISTJ", style=discord.ButtonStyle.danger)
    async def istj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ISTJ personality:",
            color=discord.Color.red()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ISTJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ISFJ", style=discord.ButtonStyle.danger)
    async def isfj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ISFJ personality:",
            color=discord.Color.red()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ISFJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ESTJ", style=discord.ButtonStyle.danger)
    async def estj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ESTJ personality:",
            color=discord.Color.red()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ESTJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ESFJ", style=discord.ButtonStyle.danger)
    async def esfj_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ESFJ personality:",
            color=discord.Color.red()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ESFJ")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class ExplorerButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="ISTP", style=discord.ButtonStyle.secondary)
    async def istp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ISTP personality:",
            color=discord.Color.greyple()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ISTP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ISFP", style=discord.ButtonStyle.secondary)
    async def isfp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ISFP personality:",
            color=discord.Color.greyple()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ISFP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ESTP", style=discord.ButtonStyle.secondary)
    async def estp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ESTP personality:",
            color=discord.Color.greyple()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ESTP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="ESFP", style=discord.ButtonStyle.secondary)
    async def esfp_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Gender",
            description="Select the gender for your ESFP personality:",
            color=discord.Color.greyple()
        )
        embed.add_field(name="Available Options", value="👨 Male\n👩 Female")
        view = GenderButtons("ESFP")
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class PersonalityButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    @discord.ui.button(label="Analyst", style=discord.ButtonStyle.primary)
    async def analyst_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Your Analyst Type",
            description="Select your specific personality type:",
            color=discord.Color.blue()
        )
        embed.add_field(name="Available Types", value="🤔 INTJ\n🧠 INTP\n👑 ENTJ\n💭 ENTP")
        view = AnalystButtons()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="Diplomat", style=discord.ButtonStyle.success)
    async def diplomat_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Your Diplomat Type",
            description="Select your specific personality type:",
            color=discord.Color.green()
        )
        embed.add_field(name="Available Types", value="🤗 INFJ\n🎨 INFP\n👥 ENFJ\n🌟 ENFP")
        view = DiplomatButtons()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="Sentinel", style=discord.ButtonStyle.danger)
    async def sentinel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Your Sentinel Type",
            description="Select your specific personality type:",
            color=discord.Color.red()
        )
        embed.add_field(name="Available Types", value="📋 ISTJ\n💝 ISFJ\n💼 ESTJ\n🤝 ESFJ")
        view = SentinelButtons()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        
    @discord.ui.button(label="Explorer", style=discord.ButtonStyle.secondary)
    async def explorer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="Choose Your Explorer Type",
            description="Select your specific personality type:",
            color=discord.Color.greyple()
        )
        embed.add_field(name="Available Types", value="🔧 ISTP\n🎨 ISFP\n🎯 ESTP\n🎭 ESFP")
        view = ExplorerButtons()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

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
