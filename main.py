import os
from src.ezcord import *


APP = 874663148374880287
TEST = 877399405056102431


bot = Bot(prefix='-', app_id=APP, guild_id=TEST, intents=Intents.all)


@bot.command(name='ping')
async def ping(ctx: Context):
    emd = Embed(description=f'**Pong: {bot.latency}ms**')
    await ctx.send(embed=emd)


@bot.event
async def on_ready():
    pass

bot.run(os.getenv('DISCORD_TOKEN'))
