import os
from src import *


APP = 874663148374880287
TEST = 877399405056102431


bot = Bot(
    prefix='-',
    app_id=APP,
    guild_id=TEST,
    intents=Intents.all,

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
    await ctx.send(text='This is working dude!', ephemeral=True)


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
async def ban(ctx: SlashContext):
    user_id = ctx.options[0].value
    reason = ctx.options[1].value
    user = ctx.guild.yield_member(user_id)
    await ctx.reply(
        text=f'{user.mention} got banned!\n**Reason: {reason}**',
        ephemeral=True
    )


@bot.cmd(name='ping')
async def ping(ctx: Context):
    embed = Embed(description=f'**Pong: {bot.latency}ms**')
    await ctx.send(text=f'`{ctx.guild.owner.any_name}`', embed=embed)


@bot.listen
async def on_ready():
    pass


@bot.listen
async def on_message(msg: Message):
    if msg.author == bot.user:
        return
    if msg.content.startswith('check'):
        await msg.reply(text='**`Done!`**')


@bot.listen
async def on_member_update(old, new):
    print('Old Nick: ', old.nick, '<|>', 'New Nick: ', new.nick)


bot.launch(os.getenv('DISCORD_TOKEN'))
