import asyncio
from functools import wraps

def slash_command(fn):
    if asyncio.iscoroutinefunction(fn):
        @wraps(fn)
        async def wrapper(*args):
            return await fn(*args)
        return wrapper




async def main(ctx:str,*, arg:list):
    return {ctx: arg}


ls = 'a'
kw = {'arg':[]}
a = asyncio.run(main.__call__(*ls,**kw))

print(a)