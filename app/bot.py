import os
import random
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='speak')
async def speak(ctx):
    responses = [
        'response 1',
        'response 2',
        'response 3',
        'response 4'
    ]

    response = random.choice(responses)
    await ctx.send(response)

bot.run(TOKEN)