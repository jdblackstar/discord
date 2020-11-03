import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
bot = commands.Bot(command_prefix='!')

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
        'f you',
        'i know you are but what am i',
        'eazi got a pen blackstar hehe'
    ]

    if message.content == 'speak':
        response = random.choice(responses)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@bot.command(name='speak')
async def speak(ctx):
    responses = [
        'hi there',
        'i\'m a bot',
        'shadowlands is gonna suck'
    ]

    response = random.choice(responses)
    await ctx.send(response)

@client.event 
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

client.run(TOKEN)
bot.run(TOKEN)