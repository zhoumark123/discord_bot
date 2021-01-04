# bot.py
from keep_alive import keep_alive
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv
from datetime import timedelta
from datetime import datetime, date
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
print("hello")

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    #await bot.get_channel(788800296813985823).send('np!')
chainPend = False
chainIds = []
chainKeys = []
chainChannels = []
sykGifs = ['https://tenor.com/view/sykkuno-gif-18778574', 
            'https://tenor.com/view/sykkuno-the-bibs-bibs-offline-tv-offlinetv-sykkuno-gif-19286194', 
            'https://tenor.com/view/sykkuno-gif-18778785',
            'https://tenor.com/view/sykkuno-the-bibs-offline-tv-wallah-wallahi-gif-19285868',
            'https://tenor.com/view/sykkuwu-sykkuno-gif-19131071', 
            'https://tenor.com/view/sykkuno-vtuber-gif-18778730']
toastGifs = ['https://tenor.com/view/disguised-toast-money-cry-im-rich-fake-cry-gif-16414116', 
            'https://tenor.com/view/disguised-toast-uwu-kawaii-gif-19271529', 
            'https://gfycat.com/leandimwittedchamois-disguisedtoast-offlinetv-pogchamp-poggers',
            'https://tenor.com/view/offline-tv-anime-disguised-toast-2d-3d-gif-14643512',
            'https://thumbs.gfycat.com/WebbedGracefulDegus-max-14mb.gif'
            ]
mykullGifs = ['https://tenor.com/view/michael-reeves-gif-18167017', 
            'https://cdn.discordapp.com/attachments/769429788493479956/788263305487581194/michael_1.gif',
            'https://cdn.discordapp.com/attachments/769429788493479956/788263612225028146/michael_2.gif',
            'https://cdn.discordapp.com/attachments/769429788493479956/788263978228776960/michael_3.gif',
            'https://cdn.discordapp.com/attachments/769429788493479956/788264317103505438/michael_5.gif'
            ]
howlGifs = ['https://tenor.com/view/serious-look-howl-howls-moving-castle-gif-3566445',
            'https://tenor.com/view/fly-coming-howls-moving-castle-anime-im-coming-gif-16780819'

            ]
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    global sykGifs, toastGifs, mykullGifs, howlGifs
    global chainIds, chainKeys, chainPend, chainChannels
    if 'howl' in message.content.lower():
        response = random.choice(howlGifs)
        await message.channel.send(response)
    elif message.content == "sykkuno":
        await message.channel.send(f'hi {message.author} here is your sykkuno gif ')
        response = random.choice(sykGifs)
        await message.channel.send(response)
    elif message.content == "toast":
        response = random.choice(toastGifs)
        await message.channel.send(response)
    elif message.content == "mykull":
        response = random.choice(mykullGifs)
        await message.channel.send(response)
    #chain
    elif message.content == "chain on":
        await message.channel.send("k, send key")
        #chainIds.append(message.id)
        def check(m):
            return m.author == message.author and m.channel == message.channel
        msg = await bot.wait_for('message', check=check)
        chainKeys.append(msg.content)
        chainChannels.append(message.channel)
        #chainPend = True
        return
    elif message.content == "chain off": 
        await message.channel.send("k")
        index = chainChannels.index(message.channel)
        chainChannels.pop(index)
        chainKeys.pop(index)
        chainIds.pop(index)
        return
    if len(chainChannels) != 0:#and chainPend == False:
        if message.channel in chainChannels and message.content != chainKeys[chainChannels.index(message.channel)]:
            await message.channel.send(f'{message.author} is sus!')
    '''elif chainPend: 
        temp = await message.channel.history(limit = 3).flatten()
        if temp[2].id in chainIds: #the third from last
            chainKeys.append(message.content)
            chainChannels.append(message.channel)
            chainPend = False'''
    await bot.process_commands(message)
def has_mention(message):
    print(message.mentions)
    print(message.role_mentions)
    return (len(message.mentions) != 0 or len(message.role_mentions) != 0)
def get_mentions(message):
    ret = []
    for user in message.mentions:
        ret.append(user.name)
    for role in message.role_mentions:
        ret.append(role.name)
    return ret

@bot.event
async def on_message_delete(message):
    print(message.content)
    print(message.created_at)
    delta = timedelta( seconds=12 )
    now = datetime.utcnow()
    if(now - message.created_at < delta and has_mention(message = message)):
        embed=discord.Embed(title="Ghost Ping Found!")
        embed.add_field(name="Sender", value=message.author)
        if(len(message.content) >= 1024):
            mentions = get_mentions(message)
            embed.add_field(name="Mentions", value=get_mentions(message))
        else: 
            embed.add_field(name="Message", value=message.content)
        
        await message.channel.send(embed=embed)

    
@bot.command(name='test')
@commands.has_role('admin')
async def test(ctx):
    await ctx.send('hello')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('okie imagine not having admin')


        
keep_alive()
bot.run(TOKEN)




