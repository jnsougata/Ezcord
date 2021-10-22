import time
import json
import asyncio
import aiohttp
import websockets
from src.utils.entity import Context
from src.slash.slashev import SlashContext
from src.events.MESSAGE_CREATE import Parser




class Socket:

    def __init__(
            self,
            secret: str,
            prefix: str,
            commands: list
    ):

        self.sent_time = 0
        self.ack_time = 0
        self.secret = secret
        self.prefix = prefix
        self.bucket = commands
        self.connection = None
        self.auth = {
            "Authorization":
                f"Bot {secret}"
        }


    async def connect(self):

        self.connection = await websockets.connect(
            'wss://gateway.discord.gg/?v=9&encoding=json'
        )
        if self.connection.open:
            print('[ Connection Established ]')
            print('[ ---------------------- ]')
            await self.sendMessage()
            return self.connection


    async def sendMessage(self):
        payload = {
                    "op": 2,
                    "d": {
                        "token": self.secret,
                        "intents": 32767,
                        "properties": {
                            '$os': "ios",
                            '$browser': 'Discord iOS',
                            '$device': 'discord.py',
                            '$referrer': '',
                            '$referring_domain': ''
                        }
                    }
                }

        await self.connection.send(json.dumps(payload))



    async def receiveMessage(self, conn):

        while True:
            x = await conn.recv()
            load = json.loads(x)

            event = load["t"]
            log = f'[ EVENT ] [ {load["t"]} ]'

            if load['op'] == 11:
                self.ack_time = round(time.time() * 1000)

            if load['op'] == 7:
                print('[op 7 received. Reconnecting...]')
                await self.reconnect()


            if event:

                if event == 'READY':
                    with open('src/socket/socket_hello.json', 'w') as f:
                        json.dump(load, f, indent = 2)

                if event  == 'GUILD_CREATE':
                    print(log)

                if event  == 'INTERACTION_CREATE':
                    print(log)
                    action = SlashContext(load['d'])

                    async with aiohttp.ClientSession() as session:

                        body = await action.parse()
                        await action.callback(session, body)


                elif event == 'MESSAGE_CREATE':
                    print(log)

                    raw = load['d']
                    ctx = Context(raw)

                    x = Parser(
                        ctx = ctx,
                        prefix = self.prefix,
                        bucket = self.bucket,
                        message = ctx.message,
                        secret = self.secret
                    )

                    value, auth = await x.process_message

                    if value:
                        async with aiohttp.ClientSession() as session:

                            await x.post(
                                Id = ctx.channel_id,
                                session = session,
                                auth = auth,
                                body = value
                            )

    async def heartbeat(self, conn):

        while True:
            await conn.send(json.dumps({"op": 1, "d": None}))
            self.sent_time = round(time.time() * 1000)
            await asyncio.sleep(42)
            print(f'[ ALIVE ][ Latency {await self.latency()}ms ]')

            with open('src/socket/cache.json', 'w') as f:
                latency = await self.latency()
                f.write(json.dumps({'latency': latency}))


    async def latency(self):
        return self.ack_time - self.sent_time

    async def reconnect(self):

        data = json.load(open('src/socket/socket_hello.json', 'r'))

        if len(data) > 0:

            session_id = data['d']["session_id"]
            seq = data['s']

            payload = {
                          "op": 6,
                          "d": {
                            "token": self.secret,
                            "session_id": session_id,
                            "seq": seq
                          }
                        }

            await self.connection.send(json.dumps(payload))
            print('[ Connection Resumed ]')
            print('[ ---------------------- ]')





