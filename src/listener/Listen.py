import time
import aiohttp
import asyncio
from src.utils.Entity import Context
from src.slash.SlashEvent import SlashContext



class Listener:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse
    ):
        self.data = response
        self.session = session
        self.auth_header = {"Authorization": f"Bot {secret}"}
        self.interval = None
        self.ws = socket
        self.start_time = 0
        self.ack_time = 0
        self.secret = secret


    @property
    def op(self):
        return int(self.data['op'])


    async def send_message(self, content:str, channel_id: int):
        await self.session.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            data = {"content": content},
            headers = self.auth_header
        )

    async def heartBeat(self, interval):
        while True:
            await asyncio.sleep(interval / 1000)
            await self.ws.send_json(
                {
                    "op": 1,
                    "d": None
                }
            )
            self.start_time = time.time() * 1000


    async def run(self):
        CODE = self.op
        DATA = self.data

        # RECEIVED DISPATCH
        if CODE == 0:
            print(f'[ {DATA["t"]} ]')
            RAW = DATA['d']
            print(RAW)

            EVENT = DATA['t']
            # CHECKING EVENT TYPE

            if EVENT == 'INTERACTION_CREATE':
                action = SlashContext(RAW)
                body = await action.buildBody()
                await action.postCallback(self.session, body)

            if EVENT == 'MESSAGE_CREATE':
                ctx = Context(RAW)
                if ctx.author.id != 874663148374880287:
                    if ctx.message.lower() == 'hi':
                        await self.send_message(
                            content=f"Hi...{ctx.author.mention}, this is an automate messgae!",
                            channel_id=ctx.channel_id
                        )

        # RECEIVED HELLO
        if CODE == 10:
            self.interval = DATA['d']['heartbeat_interval']

            # SENDING HEART BEAT
            asyncio.ensure_future(
                self.heartBeat(self.interval)
            )

            # SENDING IDENTIFICATION PAYLOAD
            await self.ws.send_json(
                {
                    "op": 2,
                    "d": {
                        "token": self.secret,
                        "intents": 513,
                        "properties": {
                            '$os': "ios",
                            '$browser': 'Discord iOS',
                            '$device': 'discord.py',
                            '$referrer': '',
                            '$referring_domain': ''
                        }
                    }
                }
            )

        # HEART BEAT ACK
        if CODE == 11:
            self.ack_time = time.time() * 1000
            print(f'[ Latency: {self.ack_time - self.start_time}ms ]')



