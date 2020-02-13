import os
import discord
import random
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from YTDLSource import YTDLSource
from time import sleep


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
okehURL = os.getenv('YOUTUBE-OKEH-URL')


class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """joins a voice channel"""
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self,ctx, *, url):
        """plays from a youtube url"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))


    @commands.command()
    async def okeh(self,ctx):
        """Everything is gonna be.. Okeh"""
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

        async with ctx.typing():
            url = okehURL
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send("You are gonna be.. okeh?")

    @commands.command()
    async def stop(self, ctx):
        """Makes the bot leave the channel. """

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='Lets make some music')


@bot.event
async def on_Ready():
    print('Logged in as {0} ({0})'.format(bot.user))

bot.add_cog(Music(bot))
bot.run(token)