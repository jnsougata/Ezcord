import os
from src.ezcord import *


APP = 874663148374880287
TEST = 877399405056102431


bot = Bot(prefix='-', app_id=APP, guild_id=TEST, intents=Intents.members)


@bot.command(name='ping')
async def ping(ctx: Context):
    emd = Embed(description=f'**Pong: {bot.latency}ms**')
    await ctx.send(embed=emd)


@bot.command(name='guild')
async def _guild(ctx: Context):
    await ctx.send(f'{ctx.guild.name}')

bot.run(os.getenv('DISCORD_TOKEN'))
