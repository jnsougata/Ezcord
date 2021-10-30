import os
from src.__init__ import *



APP = 874663148374880287
TEST = 877399405056102431
TOK = os.getenv('DISCORD_TOKEN')


bot = Bot(
    token = TOK,
    prefix = '-',
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
    em_one = Embed(
        title='Embed One',
        description=f'**Pong: {bot.latency}ms**'
    )
    em_two = Embed(
        title='Embed Two',
        description=f'Multiple embeds',
        color=0xf00534
    )
    await ctx.channel.send(embeds=[em_one, em_two])



@bot.event
async def ready():
    print('[ READY ]')



bot.start()



