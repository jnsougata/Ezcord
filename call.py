import re
from src.map import _CachedGuild



class X:
    def __init__(self, mention:str):
        self.id = int(re.findall("<@(.*?)>", mention)[0].replace('!',''))






guild = _CachedGuild.__call__(877399405056102431)

print([channel.category for  channel in guild.channels])