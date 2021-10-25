import os
from src.__init__ import *

APP = 874663148374880287
TEST = 877399405056102431
TOK = os.getenv('DISCORD_TOKEN')





async def echo(ctx:Map, phrase:str):
    await ctx.send(f'{ctx.author.mention} **{phrase.upper()}**')


async def info(ctx:Map, id:int):
    inf = ctx.guild.pull_member(int(id))
    await ctx.send(
        f'**OBJECTS:**'
        f'\n**{inf}**'
        f'\n{inf.mention}'
    )


async def pull(ctx:Map, id:int):
    inf = ctx.guild.pull_channel(int(id))
    await ctx.send(
        f'**OBJECTS:**'
        f'\n{inf.mention}'
        f'\n**Type:** `{inf.type}`'
    )



slash_one = MakeSlash()
slash_one.command(name='shit', description='this is a shit command')
slash_one.add_int_option(name='number', description='any number', required=True)
slash_one.add_str_option(name='username', description='your username', required=True)
slash_one.add_bool_option(name='double', description='if you want to double', required=False)
slash_one.add_choices(0, name='one', value = 1)
slash_one.add_choices(1, name='two', value ='twice')

commands = [echo, info, pull]
slash_commands = [slash_one]


bot = Bot(
    token = TOK,
    prefix = '>>',
    app_id = APP,
    guild_id = TEST,
    commands = commands,
    slash_commands = slash_commands,
    intents = Intents.all

)


bot.start()



