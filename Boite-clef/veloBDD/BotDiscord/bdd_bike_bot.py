import discord
import asyncio
from discord.ext import commands
# to add the bot to a server
# LINK = 'https://discord.com/api/oauth2/authorize?client_id=936666146143342682&permissions=8&scope=bot'
with open('./botToken.txt', 'r') as f:
    TOKEN = f.read()
CHANNEL_ID = open('./channel.txt',"r").readline()

async def runBot(pbContent, idChannel): #pbContent is a string, idChannel an int
    client = discord.Client()
    @client.event
    async def on_ready():
        # print('We have logged in as {0.user}'.format(client))
        channel = client.get_channel(idChannel)
        await channel.send(pbContent)
        await channel.send('shutdown')
    @client.event
    async def on_message(message):
        if message.content == 'shutdown':
            # print('shutting down here')
            client.close
    await client.start(TOKEN)