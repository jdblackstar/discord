import os
import random
import functools
import itertools
import math
import asyncio
import json

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands
from discord.utils import get

youtube_dl.utils.bug_reports_message = lambda: ''

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

##############################################
########## BOT EVENTS (DEPRECIATED) ##########
##############################################

# # bot even to post a successful connection to stdout
# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')

# bot event to let a user know that they don't have the proper role
# for a specific bot command
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send('You do not have the correct role for this command.')

#########################################################
########## ADMINISTRATIVE AND MODERATION TOOLS ##########
#########################################################

class Administrative(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def addmuted(self, ctx: commands.Context):
        if get(ctx.guild.roles, name='muted'):
            print('muted role already exists')
        else:
            await ctx.guild.create_role(name='muted', color=discord.Color('0xff0000'))
            print('muted role created')

    @commands.command(name='addrole', pass_context=True)
    @commands.has_any_role('admin', 'moderator', 'owner', 'Admin')
    async def addrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        '''
        Assigns a specific user (member) a specific role. Can only be used by admins and mods
        '''
        await member.add_roles(role)
        await ctx.send(f'{member.name} has been given the \'{role.name}\' role by {ctx.author.name}.')


    @commands.command(name='mute', pass_context=True)
    @commands.has_any_role('admin', 'moderator', 'owner', 'Admin')
    async def mute(self, ctx: commands.Context, member: discord.Member, mute_time: int, reason=None):
        '''
        Mutes a specific member, for an amount of seconds. Can optionally give a reason.
        Can only be used by admins and moderators.

        Also sends a DM with information on the mute; who applied it, for how long
        and what the reason was (if there was one)
        '''
        #TODO - check for the muted role and add it if it's missing
        # maybe we can do this in an initial 'setup' command when the bot first joins the server

        # the role we'll be giving the 'muted' person
        role = discord.utils.get(ctx.guild.roles, name='muted')

        # this should check if the member has "admin" privileges of the server
        '''
        if 
            # if they do NOT, do the muting thing i wrote
            await member.add_roles(role)
            # embed stuff
            embed = discord.Embed(color=discord.Color.green())
            embed.add_field(name=f'You\'ve been **Muted in {ctx.guild.name}.', value=f'**Action By: **{ctx.author.mention}\n**Reason: **{reason}\n**Duration:** {mute_time}')
            await member.send(embed=embed)
            # give 'muted' role for {mute_time} num of seconds
            await ctx.sned(f'{member.name} muted for {mute_time} seconds by {ctx.author.name}.')
            await asyncio.sleep(mute_time)
            await member.remove_roles(role)
            await ctx.send(f'{member.name} has been unmuted.')
        elif discord.utils.get(ctx.guild.roles, name='muted') in member.roles:
            # response if admin tries to mute someone that's already muted
            # don't know how to add time to an asyncio window yet
            await ctx.send(f"{member.name} is already muted.")
        else:
            # someone with incorrect permissions tries to use !mute
            await ctx.send("Cannot mute an administrative user.")

        # if discord.utils.get(ctx.guild.roles, name='admin') in member.roles:
        #     await ctx.send("Nah, can't mute an admin.")
        # if discord.utils.get(ctx.guild.roles, name='Admin') in member.roles:
        #     await ctx.send("Nah, can't mute an admin.")
        # if discord.utils.get(ctx.guild.roles, name='Owner') in member.roles:
        #     await ctx.send("Nah, not gonna mute that guy.")
        # elif discord.utils.get(ctx.guild.roles, name='moderator') in member.roles:
        #     await ctx.send("Nah, can't mute a moderator.")
        # elif discord.utils.get(ctx.guild.roles, name='BSBot') in member.roles:
        #     await ctx.send("I'm not gonna mute myself...")
        # elif discord.utils.get(ctx.guild.roles, name='muted') in member.roles:
        #     await ctx.send(f"{member.name} is already muted.")
        # else:
        #     await member.add_roles(role)

        #     embed = discord.Embed(color=discord.Color.green())
        #     embed.add_field(name=f'You\'ve been **Muted** in {ctx.guild.name}.', value=f'**Action By: **{ctx.author.mention}\n**Reason: **{reason}\n**Duration:** {mute_time}')
        #     await member.send(embed=embed)

        #     await ctx.send(f'{member.name} muted for {mute_time} seconds by {ctx.author.name}.')
        #     await asyncio.sleep(mute_time)
        #     await member.remove_roles(role)
        #     await ctx.send(f'{member.name} has been unmuted.')
    '''

    # @commands.command(name='mute')
    # @commands.command(pass_context = True)
    # async def mute(self, ctx: commands.Context, member: discord.Member):
    #     if ctx.message.author.server_permissions.administrator or ctx.message.author.id == '194151340090327041':
    #         role = discord.utils.get(member.server.roles, name='Muted')
    #         await bot.add_roles(member, role)
    #         embed=discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)
    #         await bot.say(embed=embed)
    #     else:
    #         embed=discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6)
    #         await bot.say(embed=embed)


    @commands.command(name='create-channel')
    @commands.has_any_role('admin', 'Admin', 'Owner')
    async def create_channel(self, ctx: commands.Context, channel_name='bot-test-2'):
        '''
        Method to create a channel with a specific name.
        Not sure how useful this is, because you can't put it in a category (or inherit permissions)
        '''
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')
            await guild.create_text_channel(channel_name)


    # @commands.command(name='delete-channel')
    # @commands.has_role('admin')
    # async def create_channel(self, ctx: commands.Context, channel_name=None):
    #     guild = ctx.guild
    #     existing_channel = discord.utils.get(guild.channels, name=channel_name)
    #     if existing_channel:
    #         print(f'Deleting the specifid channel: {channel_name}')
    #         await guild.delete_text_channel(channel_name)
    #     else:
    #         print(f'Channel {channel_name} not found.')


#######################################################
########## MUSIC BOT ATTEMPT BELOW THIS LINE ##########
#######################################################

class VoiceError(Exception):
    pass

class YTDLError(Exception):
    pass

class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break
            
            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)

class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed

class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]

class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self.ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                try:
                    async with timeout(180): #180 seconds = 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        '''
        Joins the invoking member's current voice channel.
        '''
        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        '''
        Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        '''
        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        '''
        Clears the queue and leaves the voice channel.
        '''
        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        '''
        Sets the volume of the player.
        '''
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        '''
        Displays the currently playing song.
        '''
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        '''
        Pauses the currently playing song.
        '''
        if ctx.voice_state.voice.is_playing():   # and ctx.voice_state.voice.is_playing()
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        '''
        Resumes a currently paused song.
        '''
        if ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        '''
        Stops playing song and clears the queue.
        '''
        ctx.voice_state.songs.clear()

        if ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        '''
        Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        '''
        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        '''
        Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        '''

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        '''
        Shuffles the queue.
        '''
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        '''
        Removes a song from the queue at a given index.
        '''
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        '''
        Loops the currently playing song.
        Invoke this command again to unloop the song.
        '''
        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        '''
        Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        '''

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

#######################################################
########## MISC BOT COMMANDS BELOW THIS LINE ##########
#######################################################

# Economy class contains all methods related to the server's 'money'
# possibly even RDS stuff, but I'll need to consult someone on that
class Economy(commands.Cog):
    '''
    Economy class to allow users to have a 'balance' of money.

    methods needed:
    - on_join
    - on_message
    - check_balance
    - pay (probably reserved for admin to grant money)
    - request (?)

    Thinking about using an RDS to keep track of users' money. Will need some help with that,
    most likely.

    For solo bets:
    - decided by coin flip
    - no trusted party needed to confirm/reject the outcome of a bet

    For multiple party bets:
    two scenarios:
    - bet on real life event
        - outcome determined by manual input (verified person only)
    - random chance bet
        - coin flip, but maybe more exciting
            - think death roll from WoW, can explain if needed
        - number guessing? idk
    '''

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='on_join')
    async def on_join(self, ctx: commands.Context):
        ...

    @commands.command(name='on_message')
    async def on_message(self, ctx: commands.Context):
        ...

    @commands.command(name='balance')
    async def check_balance(self, ctx: commands.Context):
        '''
        Tells the user their current balance of points.
        '''
        ...

    @commands.command(name='xbalance')
    async def check_user_balance(self, ctx: commands.Context, member: discord.Member):
        '''
        Shows the balance of a specific member - probably only used by admins and mods
        '''
        ...

    @commands.command(name='pay')
    async def pay_user(self, ctx: commands.Context, member: discord.Member, amount: int):
        '''
        Transfers points from the user's balance to the specific member's balance
        Maybe add a default amount?
        '''
        ...

    @commands.command(name='charge')
    async def charge_user(self, ctx: commands.Context, member: discord.Member, amount: int):
        '''
        Requests a payment from a specific member's
        '''
        ...


# Gamble class contains all methods related to gambling (duh)
class Gamble(commands.Cog):
    '''
    Gamble methods:
    - roll: rolls num_dice with num_sides
    - bet(house): place a bet, flip a coin, get 2x if you win, lose all if you lose
    - start_bet: starts a bet with a description, buy-in amount, duration (?)
        - if another member types '!join', they'll accept the odds
        - verified user (moderator+ will have to confirm the outcome of the bet, as it
          will likely be tied to a real life event and LMAO if you think I'm gonna be
          coding all that shit)

    - STRETCH: implement blackjack
    '''
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # maybe add unload method here? (i don't know what an unload method is)

    @commands.command(name='roll')
    async def roll(self, ctx: commands.Context, num_dice: int, num_sides: int):
        '''
        Rolles a num_dice number of dice with num_sides number of sides
        '''
        dice = [
            str(random.choice(range(1, num_sides + 1)))
            for _ in range(num_dice)
        ]
        await ctx.send(', '.join(dice))


    @commands.command(name='bet_npc')
    async def bet_npc(self, ctx: commands.Context, amount: int):
        '''
        rolls 1-100
        even number, member's amount entered is doubled
        odd number, member's amount entered is subtracted from balance
        '''
        ...

# Speak class contains methods that return purely strings (jokes, one-liners, etc.)
class Speak(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='speak')
    @commands.has_any_role('admin', 'moderator', 'friend')
    async def rand_response(self, ctx: commands.Context):
        '''
        Returns a random response from the list below
        Would like to expand on this and do some NLP maybe
        '''
        responses = [
            'response 1',
            'response 2',
            'response 3',
            'response 4',
            'response 5',
            'response 6',
            'response 7',
            'response 8',
            'response 9',
            'response 10'
        ]

        response = random.choice(responses)
        await ctx.send(response)

    @commands.command(name='choose')
    async def choose(self, ctx: commands.Context, *choices: str):
        await ctx.send(random.choice(choices))


############################################
########## ADD BOT COGS (MODULES) ##########
############################################

bot = commands.Bot('!', description='The best, all purpose bot.')

bot.add_cog(Administrative(bot))
bot.add_cog(Music(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Gamble(bot))
bot.add_cog(Speak(bot))

##########################################
########## UNIVERSAL BOT EVENTS ##########
##########################################

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)