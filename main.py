import os
from src.droid.Driod import Bot
from src.slash.ext import Slash, Builder

app = 874663148374880287
test = 877399405056102431

async def zen(ctx):
    return 'Are you talking about my boss?'

scmd = Builder()
scmd.command(name='shit', description='this is a shit command')
scmd.add_int_option(name='number', description='any number', required=True)
scmd.add_str_option(name='username', description='your username', required=True)
scmd.add_bool_option(name='double', description='if you want to double', required=False)
scmd.add_choices(0, name='one', value = 1)
scmd.add_choices(1, name='two', value = 'twice')

slash = Slash(
    scmd = scmd.json,
    application_id = app,
    guild_id = test
)

commands = [zen]

bot = Bot(
    token = os.getenv('DISCORD_TOKEN'),
    commands = commands,
    prefix = '-',
    add_slash = [slash]
)

bot.start()



