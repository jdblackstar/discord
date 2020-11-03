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

@bot.command(name='roll')
async def roll(ctx, num_dice: int, num_sides: int):
    dice = [
        str(random.choice(range(1, num_sides + 1)))
        for _ in range(num_dice)
    ]
    await ctx.send(', '.join(dice))

bot.run(TOKEN)