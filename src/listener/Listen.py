import aiohttp
from src.utils.entity import Context
from src.command.msg_to_cmd import Parser
from src.slash.slashev import SlashContext



class Listener:

    def __init__(
            self,
            secret: str,
            response: dict,
            session: aiohttp.ClientSession,
            socket: aiohttp.ClientWebSocketResponse,
            bucket: list,
    ):
        self.data = response
        self.session = session
        self.auth_header = {"Authorization": f"Bot {secret}"}
        self.ws = socket
        self.start_time = 0
        self.ack_time = 0
        self.secret = secret
        self.bucket = bucket


    @property
    async def op(self):
        return int(self.data['op'])


    async def send_message(self, content:str, channel_id: int):
        await self.session.post(
            f'https://discord.com/api/v9/channels/{channel_id}/messages',
            data = {"content": content},
            headers = self.auth_header
        )


    async def run(self):
        CODE = await self.op
        DATA = self.data

        # RECEIVED DISPATCH
        if CODE == 0:
            EVENT = DATA['t']
            print(f'[ {EVENT} ]')
            RAW = DATA['d']
            print(DATA)

            # CHECKING EVENT TYPE

            if EVENT == 'INTERACTION_CREATE':
                action = SlashContext(RAW)
                body = await action.parse()
                await action.callback(self.session, body)

            if EVENT == 'MESSAGE_CREATE':
                ctx = Context(RAW)
                if ctx.author.id != 874663148374880287:
                    if ctx.message.lower() == 'hi':
                        await self.send_message(
                            content=f"Hi...{ctx.author.mention}, this is an automate messgae!",
                            channel_id=ctx.channel_id
                        )

                    PARSER = Parser(
                        ctx = ctx,
                        prefix = '-',
                        secret = self.secret,
                        bucket = self.bucket
                    )
                    body = await PARSER.process_message

                    await PARSER.post(
                        auth = self.auth_header,
                        body = body,
                        session = self.session
                    )

        # RECEIVED HELLO
        elif CODE == 10:

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
        elif CODE == 11:
            EVENT = DATA['t']
            print(f'[ {EVENT} ]')
            print(DATA)

        else:
            print(DATA)
