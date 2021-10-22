import os
from src.droid.Driod import Bot
from src.slash.SlashHandler import Slash



slash = Slash(
    application_id = 874663148374880287,
    guild_id = 877399405056102431,
)

slash.create_command(
    name = 'hiiii',
    description = 'cya... nest time'
)
slash.add_string_option(
    name = "fucking",
    description = 'IDGF',
    required = True
)


async def zen(ctx):
    return 'Are you talking about my boss?'




commands = [zen]

bot = Bot(
    token = os.getenv('DISCORD_TOKEN'),
    commands = commands,
    prefix = '-',
    add_slash = slash
)

bot.start()



