import json
from aiohttp import ClientSession

class Stack:
    def __init__(self, raw_json:dict):
        self.__data = raw_json


    async def hello(self):
        PATH = "src/stack/hello_stack.json"
        with open(PATH, 'w') as f:
            json.dump(obj=self.__data, fp=f, indent=2, sort_keys=True)


    async def guild(self):
        GUILD_ID = self.__data['d']['id']
        PATH = "src/stack/guild_stack.json"
        data = json.load(open(PATH, 'r'))
        data[str(GUILD_ID)] = self.__data
        with open(PATH, 'w') as f:
            json.dump(obj=data, fp=f, indent=4, sort_keys=True)


    @staticmethod
    async def latency(value):
        PATH = "src/stack/latency_stack.json"
        with open(PATH, 'w') as f:
            json.dump(obj={'latency': value}, fp=f, indent=2, sort_keys=True)


    async def ready(self):
        PATH = "src/stack/ready_stack.json"
        with open(PATH, 'w') as f:
            json.dump(obj=self.__data, fp=f, indent=2, sort_keys=True)


    async def slash(self):
        CMD_ID = self.__data['id']
        PATH = "src/stack/slash_stack.json"
        data = json.load(open(PATH, 'r'))
        data[str(CMD_ID)] = self.__data
        with open(PATH, 'w') as f:
            json.dump(obj=data, fp=f, indent=2, sort_keys=True)


    @staticmethod
    async def members(session:ClientSession, auth_header:dict, guild_id:int):
        endpoint = f'/guilds/{guild_id}/members?limit=100'
        PATH = "src/stack/member_stack.json"
        resp = await session.get(
            'https://discord.com/api/v9/' + endpoint,
            headers = auth_header
        )

        member_list = await resp.json()
        js = json.load(open(PATH, 'r'))
        temp = dict()
        for item in member_list:
            USER_ID = item['user']['id']
            temp[str(USER_ID)] = {str(USER_ID): item}
        with open(PATH, 'w') as f:
            js[str(guild_id)] = temp
            json.dump(obj = js,fp = f,indent = 2,sort_keys = True)

