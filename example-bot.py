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
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
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
            if client.user in message.mentions:
                await message.channel.send('You mentioned me!')
                
            # 2b: Message is a reply to the bot
            elif message.reference and message.reference.resolved.author == client.user:
                await message.channel.send('You replied to me!')

    except discord.errors.Forbidden:
        print(f"Missing permissions in channel: {message.channel.name}")

client.run(os.getenv('DISCORD_TOKEN'))
