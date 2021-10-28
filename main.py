import os
from src.__init__ import *

APP = 874663148374880287
TEST = 877399405056102431
TOK = os.getenv('DISCORD_TOKEN')


bot = Bot(
    token = TOK,
    prefix = 'e!',
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
async def region(ctx:Context):
    await ctx.send(text=f'**{ctx.guild.region}**')

@bot.command
async def ping(ctx:Context):
    await ctx.send(text='pong')


@bot.command
async def info(ctx:Context):
    guild = ctx.guild
    text = f"**author:** `{ctx.author}`" \
           f"\n**server**: {guild.name}" \
           f"\n**id**: {guild.id}" \
           f"\n**member count**: {guild.member_count}" \
           f"\n**slash commands**: {guild.slash_count}" \
           f"\n**total boosts**: {guild.boost_level}" \
           f"\n**banner hash**: {guild.banner}" \
           f"\n**content filter**: {guild.content_filter}" \
           f"\n**alert level**: {guild.alert_level}" \
           f"\n**animated**: {guild.flags.ANIMATED}" \
           f"\n**icon hash**: {guild.icon}"

    await ctx.send(text = text)



bot.start()



