import os

import src.message
from src.__init__ import *
import discord


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




rate = Slash(name='rate', description='rate me out of 5')
rate.add_options([
    rate.set_int_option(
        name='ratings',
        description='choose ratings',
        choices=[
            rate.set_choice(name='★', value=1),
            rate.set_choice(name='★★', value=2),
            rate.set_choice(name='★★★', value=3),
            rate.set_choice(name='★★★★', value=4),
            rate.set_choice(name='★★★★★', value=5)
        ],
        required=True
    ),
    rate.set_str_option(
        name='feedback',
        description='choose ratings',
        choices=[],
        required=False
    )
])
@bot.slash_cmd(command=rate)
async def rate(ctx: SlashContext):
    await ctx.send(text='This is working dude!')



ban = Slash(name='ban', description='bans a member')
ban.add_options([
    ban.set_user_option(
        name='user',
        description='this user will be banned!',
        required=True,
    ),
    ban.set_str_option(
        name='reason',
        description='reason why the user get banned',
        required=True

    )
])


@bot.slash_cmd(command=ban)
async def ban(ctx:SlashContext):
    user_id = ctx.options[0].value
    reason = ctx.options[1].value
    user = ctx.guild.pull_member(user_id)
    await ctx.reply(
        text=f'{user.mention} got banned!\n**Reason: {reason}**'
    )


@bot.cmd
async def ping(ctx:Context):
    await ctx.send(text='pong')


@bot.event
async def ready(payload: dict):
    print(payload)

@bot.event
async def message_create(msg: Message):
    if msg.author.id == msg.guild.owner.id:
        await msg.reply(text=f'{msg.author.mention} hi boss!')


@bot.event
async def message_update(payload: dict):
    print(payload)



bot.start()



