import json
from aiohttp import ClientSession

class Stack:
    def __init__(self, raw_json:dict):
        self.__data = raw_json


    async def hello(self):
        PATH = "src/stack/hello_stack.json"
        with open(PATH, 'w') as f:
            self.__data['l'] = 0
            json.dump(obj=self.__data, fp=f, indent=2, sort_keys=True)


    async def guild(self):
        GUILD_ID = self.__data['d']['id']
        PATH = "src/stack/guild_stack.json"
        data = json.load(open(PATH, 'r'))
        data[str(GUILD_ID)] = self.__data
        with open(PATH, 'w') as f:
            json.dump(obj=data, fp=f, indent=4, sort_keys=True)



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


    async def members(self):
        PATH = "src/stack/guild_stack.json"
        member_list = self.__data['d']['members']
        js = json.load(open(PATH, 'r'))
        temp = dict()
        for item in member_list:
            USER_ID = item['user']['id']
            temp[str(USER_ID)] = item
        with open(PATH, 'w') as f:
            js[str(self.__data['d']['guild_id'])]["m"] = temp
            json.dump(obj = js,fp = f,indent = 2, sort_keys = True)

