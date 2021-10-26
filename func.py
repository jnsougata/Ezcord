import asyncio
from functools import wraps

def slash_command(fn):
    if asyncio.iscoroutinefunction(fn):
        @wraps(fn)
        async def wrapper():
            return await fn()
        return wrapper



@slash_command
async def main():
    return {1: 'x'}


print(asyncio.run(main()))