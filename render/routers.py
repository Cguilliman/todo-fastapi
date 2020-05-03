import asyncio
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

import aioredis
from aioredis.errors import ConnectionClosedError as ServerConnectionClosedError


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
XREAD_TIMEOUT = 0
XREAD_COUNT = 100
NUM_PREVIOUS = 30
STREAM_MAX_LEN = 1000
ALLOWED_ROOMS = ['chat:1', 'chat:2', 'chat:3', 'leonfeed']
PORT = 8080
HOST = "0.0.0.0"


async def get_redis_pool():
    try:
        pool = await aioredis.create_redis_pool(
            (REDIS_HOST, REDIS_PORT), encoding='utf-8')
        return pool
    except ConnectionRefusedError as e:
        print('cannot connect to redis on:', REDIS_HOST, REDIS_PORT)
        return None


async def get_chat_history():
    pass


router = APIRouter()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
def main_page():
    return HTMLResponse(html)


async def ws_send(websocket: WebSocket):
    """
    wait for new items on chat stream and
    send data from server to client over a WebSocket
    :param websocket:
    :type websocket:
    """
    pool = await get_redis_pool()
    latest_ids = ['$']
    ws_connected = True
    while pool and ws_connected:
        try:
            events = await pool.xread(
                streams=['1'],
                count=XREAD_COUNT,
                timeout=XREAD_TIMEOUT,
                # latest_ids=latest_ids
            )
            for _, e_id, event in events:
                event['e_id'] = e_id
                await websocket.send_json(event)
                # latest_ids = [e_id]
        except ConnectionClosedError:
            ws_connected = False

        except ConnectionClosedOK:
            ws_connected = False

        except ServerConnectionClosedError:
            print('redis server connection closed')
            return
    pool.close()


async def ws_receive(websocket: WebSocket):
    """
    receive json data from client over a WebSocket, add messages onto the
    associated chat stream
    :param websocket:
    :type websocket:
    """
    print("RECEIVE")
    ws_connected = False
    pool = await get_redis_pool()
    added = await pool.sadd("1:user", 'a')
    if added:
        ws_connected = True
    else:
        await pool.srem("1:user", "a")
        print('duplicate user error')
        added = await pool.sadd("1:user", 'a')
    print('BEFORE', added)

    while added:
        try:
            data = await websocket.receive_text()
            print(data)
            fields = {
                'uname': 'a',
                'msg': str(data),  # data['msg'],
                'type': 'comment',
                'room': '1'
            }
            await pool.xadd(
                stream='1',
                fields=fields,
                message_id=b'*',
                max_len=STREAM_MAX_LEN
            )
        except WebSocketDisconnect:
            await pool.srem("1:user", "1")
            # await announce(pool, chat_info, 'disconnected')
            ws_connected = False

        except ServerConnectionClosedError:
            print('redis server connection closed')
            return

        except ConnectionRefusedError:
            print('redis server connection closed')
            return
    pool.close()


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     # check the user is allowed into the chat room
#     # open connection
#     await websocket.accept()
#     await asyncio.gather(
#         ws_receive(websocket),
#         ws_send(websocket)
#     )
