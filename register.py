from src.slash.SlashHandler import Slash


slash = Slash(
    application_id = 874663148374880287,
    guild_id = 877399405056102431,
)

slash.create_command(
    name = 'bye',
    description = 'cya'
)
slash.add_string_option(
    name = "fucking",
    description = 'IDGF',
    required = True
)
print(slash.json)