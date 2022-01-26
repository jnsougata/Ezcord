import os
from src.ezcord import *


APP = 874663148374880287
TEST = 877399405056102431


bot = Bot(prefix='-', app_id=APP, guild_id=TEST, intents=Intents.members)


@bot.command(name='ping')
async def ping(ctx: Context):
    emd = Embed(description=f'**Pong: {bot.latency}ms**')
    await ctx.reply(embed=emd)


@bot.command(name='foo')
async def _foo(ctx: Context):
    await ctx.send(f'{bot.user()}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'------')

bot.run(os.getenv('DISCORD_TOKEN'))
