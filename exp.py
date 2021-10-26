import re
import json
import inspect
from src.map import _CachedGuild


#int(re.findall("<@(.*?)>", mention)[0].replace('!',''))


string = '!g 899930155361919028'
args = string.split(' ')
args.remove('!g')
args = [i for i in args if i != '']


def command(function):
    classes = [int, str, float, _CachedGuild]
    i = inspect.signature(function)
    params = i.parameters
    types = [str(params.get(key).annotation) for key in params]

    # fix kw args ls = [str(params.get(arg).kind) for arg in params]

    final = []
    for i in range(len(types)):
        for x in classes:
            if x.__name__ in types[i]:
                final.append(x(args[i]))
    val = function.__call__(*final)
    print(val)
    return val







@command
def func(a: _CachedGuild):
    return len(a.members)
