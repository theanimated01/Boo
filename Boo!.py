import discord
import json
import random
import os
from discord.ext import commands
from discord.utils import get

def get_prefix(client, message):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix = get_prefix)
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('-help'))
    

@client.event
async def on_guild_join(guild):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '-'

    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f)

@client.event
async def on_guild_remove(guild):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f)

@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('Prefixes.json', 'w') as f:
        json.dump(prefixes, f)

    await ctx.send(f'Successfully changed prefix to {prefix} !')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing argument, please try again with all required arguments')

@client.command()
async def help(ctx):

    embed = discord.Embed(
        color= discord.Color.purple()
    )

    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/809469105789993032/2348d58f6dd45965dd884a70ebcfcf26.png?size=256')
    embed.set_author(name='HELP', icon_url='https://cdn.discordapp.com/avatars/809469105789993032/2348d58f6dd45965dd884a70ebcfcf26.png?size=256')
    embed.add_field(name='ping', value='gives the ping of the bot', inline=False)
    embed.add_field(name='prefix', value='can be used to change prefix of bot (can be used by administrators only)', inline=False)
    embed.add_field(name='hi', value='just says hi, or maybe try mentioning someone ;)', inline=False)
    embed.add_field(name='luv', value='spread luv in the server or to a specific person', inline=False)
    embed.add_field(name='8ball', value='just your standard 8ball', inline=False)
    embed.add_field(name='clear', value='clears a particular amount of messages. (must have manage message permission)', inline=False)
    embed.add_field(name='idjot', value='Your standard idjot command to call someone an IDJOT. kekw', inline=False)

    await ctx.send(embed=embed)
 
@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command(aliases=['hey','hello'])
async def hi(ctx, mem=None):
    if mem==None:
        await ctx.send(f'Hello IDJOT!')
    else:
        await ctx.send(f'Hello IDJOT! {mem}')

@client.command()
async def luv(ctx, mem=None):
    if mem == None:
        await ctx.send('Spreading luv to everyone in the server')
        await ctx.send(f'<:pinqhairluv:810930016002375701>')
    else:
        await ctx.send(f'You have sent luv to {mem}')
        await ctx.send('<:pinqhairluv:810930016002375701>')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses=['Yes', 'You can rely on it', 'All signs point to yes',
               'Eh, maybe', 'Cannot predict now', 'Concentrate and ask again',
               'I would say no', 'Nah', 'All signs point to no']
    await ctx.send(f'{random.choice(responses)}')

@client.command(aliases=['delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'Successfully deleted {amount} message')

@client.command()
async def idjot(ctx, mem=None):
    if mem==None:
        await ctx.send('You are an IDJOT!')
        #await ctx.send(f'<:KEKW:795870448549101568>')
    else:
        await ctx.send(f'{mem} is an IDJOT!')
    

client.run(str(os.environ.get('token')))
