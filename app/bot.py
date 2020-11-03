import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, please remember to choose a role."
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    responses = [
        'fuck you',
        'i know you are but what am i',
        'eazi got a pen blackstar hehe'
    ]

    if message.content == 'speak':
        response = random.choice(responses)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

client.run(TOKEN)