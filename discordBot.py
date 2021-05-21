# bot.py
import os

import discord
from discord import channel
from dotenv import load_dotenv

from bot import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

print(TOKEN)

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for g in client.guilds:
        if(g.name == GUILD):
            break
        else:
            print(f'{g.name} (id: {g.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    testMessage = ['WAZZUP!']

    if message.content == 'hello!':
        response = message.author.name
        print(len(response))
        await message.channel.send(f'WAZZUP {response}!')



client.run(TOKEN)
