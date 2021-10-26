import os
from src.__init__ import *

APP = 874663148374880287
TEST = 877399405056102431
TOK = os.getenv('DISCORD_TOKEN')


bot = Bot(
    token = TOK,
    prefix = '>>',
    app_id = APP,
    guild_id = TEST,
    intents = Intents.members,

)

@bot.slash_command
async def slash_one():

    slash = Slash(
        name='rate',
        description='please rate me out of 5',
    )
    slash.add_options([
        slash.set_int_option(
            name='ratings',
            description='choose ratings',
            choices=[
                slash.set_choice(name='★', value=1),
                slash.set_choice(name='★★', value=2),
                slash.set_choice(name='★★★', value=3),
                slash.set_choice(name='★★★★', value=4),
                slash.set_choice(name='★★★★★', value=5)
            ],
            required=True
        ),
        slash.set_str_option(
            name='feedback',
            description='choose ratings',
            choices=[],
            required=False
        )
    ])
    return slash.json


@bot.slash_command
async def slash_two():
    slash = Slash(
        name='ban',
        description='bans a member'
    )
    slash.add_options([
        slash.set_user_option(
            name='user',
            description='this user will be banned!',
            required=True,
        ),
        slash.set_str_option(
            name='reason',
            description='reason why the user get banned',
            required=True

        )
    ])
    return slash.json


@bot.command
async def ping(ctx:Context):
    await ctx.send(text=f'{await bot.latency}ms!')






bot.start()



