import os
from src.__init__ import *

APP = 874663148374880287
TEST = 877399405056102431
TOK = os.getenv('DISCORD_TOKEN')


bot = Bot(
    token = TOK,
    prefix = '!!',
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
@bot.slash_command(command=rate)
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

@bot.slash_command(command=ban)
async def ban(ctx:SlashContext):
    user_id = ctx.options[0].value
    reason = ctx.options[1].value
    user = ctx.guild.pull_member(user_id)
    await ctx.reply(text=f'{user.mention} got banned!\n**Reason: {reason}**')
    await ctx.send(ctx.channel.mention)



@bot.command
async def ping(ctx:Context):
    await ctx.send(text='pong')


@bot.command
async def info(ctx:Context):
    guild = ctx.guild
    text = f"**author:** `{ctx.author}` {ctx.author.mention}" \
           f"\n\n**server:** `{guild.name}`" \
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



