import os
from src.ezcord import *


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


@bot.slash_command(command=rate)
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


@bot.slash_command(command=ban)
async def ban(ctx: SlashContext):
    user_id = ctx.options[0].value
    reason = ctx.options[1].value
    user = ctx.guild.get_member(user_id)
    await ctx.reply(
        text=f'{user.mention} got banned!\n**Reason: {reason}**',
        ephemeral=True
    )


@bot.command(name='ping')
async def ping(ctx: Context):
    emd = Embed(description=f'**Pong: {bot.latency}ms**')
    await ctx.send(text=f'`{ctx.guild.owner.any_name}`', embed=emd)


@bot.event
async def on_ready():
    pass


@bot.event
async def on_message(msg: Message):
    if msg.author == bot.own:
        return
    if msg.content.startswith('check'):
        await msg.reply(text='**`Done!`**')

bot.run(os.getenv('DISCORD_TOKEN'))
