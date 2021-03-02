import discord
import json
import random
import youtube_dl
import requests
import os
import ctypes
import ctypes.util
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio


def get_prefix(client, message):
    with open('Prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('-help'))
    print('Bot is ready')


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
    embed.add_field(name='play or p', value='Plays a song (does not work with spotify yet)', inline=False)
    embed.add_field(name='queue or q', value='Add a song to queue', inline=False)
    embed.add_field(name='pause or pa', value='Pauses the song currently playing', inline=False)
    embed.add_field(name='resume or r', value='Resumes the song currently playing', inline=False)
    embed.add_field(name='skip or s', value='Skips the song playing and plays next song in queue', inline=False)
    embed.add_field(name='leave or disconnect or dc', value='Disconnects the bot from VC', inline=False)

    await ctx.send(embed=embed)


@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')


@client.command(aliases=['hey', 'hello'])
async def hi(ctx, mem=None):
    if mem == None:
        await ctx.send(f'Hello IDJOT!')
    else:
        await ctx.send(f'Hello IDJOT! {mem}')


@client.command()
async def luv(ctx, mem=None):
    if mem == None:
        await ctx.send('Spreading luv to everyone in the server')

    else:
        await ctx.send(f'You have sent luv to {mem}')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['Yes', 'You can rely on it', 'All signs point to yes',
                 'Eh, maybe', 'Cannot predict now', 'Concentrate and ask again',
                 'I would say no', 'Nah', 'All signs point to no']
    await ctx.send(f'{random.choice(responses)}')


@client.command(aliases=['delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'Successfully deleted {amount} message')


@client.command()
async def idjot(ctx, mem=None):
    if mem == None:
        await ctx.send(f'You are an IDJOT!')
    else:
        await ctx.send(f'{mem} is and IDJOT!')


@client.command(aliases=['dc', 'disconnect'])
async def leave(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(':mailbox_with_no_mail: **Successfully disconnected**')
    else:
        await ctx.send('I am not in any voice channel currently')


def search(query):

    with ytdl:
        try:
            requests.get(query)
        except:
            info = ytdl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else:
            info = ytdl.extract_info(query, download=False)
    return info, info['formats'][0]['url']

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

}

ytdl = youtube_dl.YoutubeDL(ydl_opts)

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

@client.command(aliases=['p'])
async def play(ctx, *, url):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        pass
    else:
        voice = await channel.connect()
        await ctx.send(f'Successfully joined `{channel}`')

    if voice.is_playing():
        await ctx.send('Already playing a song. Try using -q or -queue to queue a song :thumbsup:')
    else:
        await ctx.send(f'Searching for: `{url}` :mag_right:')
        video, source = search(url)
        voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: check_queue())
        voice.is_playing()
        await ctx.send(f'Playing: :notes: `{video["title"]}` - Now!')


def check_queue():

    voice = get(client.voice_clients)
    if len(queue) == 0:
        pass
    else:
        next_song = queue.pop(0)
        video, source = search(next_song)
        voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: check_queue())
        voice.is_playing()


@client.command(aliases=['q'])
async def queue(ctx, *, url):

    await ctx.send(f'Searching: :mag_right: `{url}`')
    video, source = search(url)
    await ctx.send(f'Found `{video["title"]}` :thumbsup:')
    queue.append(video['title'])

    embed = discord.Embed(
        color=discord.Color.dark_gray()
    )
    embed.set_author(name='Added to queue')
    embed.add_field(name='Name', value=queue[0])

    await ctx.send(embed=embed)


@client.command(aliases=['pa'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('**Paused** :pause_button:')


@client.command(aliases=['r'])
async def resume(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send('**Resuming** :play_pause:')


@client.command(aliases=['s'])
async def skip(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)
    if len(queue) == 0:
        await ctx.send('No song in queue to skip to')
    else:

        next_song = queue.pop(0)
        video, source = search(next_song)
        voice.stop()
        await ctx.send('**Skipped** :thumbsup:')
        await ctx.send(f'Playing :notes: `{video["title"]}` - Now!')
        voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: check_queue())
        voice.is_playing()


queue = []
client.run(str(os.environ.get('token'))

