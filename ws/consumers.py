from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from sqlalchemy.orm import Session
from fastapi import APIRouter, WebSocket, Depends

import aioredis
from aioredis.errors import ConnectionClosedError as ServerConnectionClosedError

from contrib.auth.auth import get_current_user_or_anonymous
from models import get_db, User
from contrib.chat import create_message, build_chat_message
from .schemas import MessageSchema


router = APIRouter()
# Remove to some settings module
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
XREAD_TIMEOUT = 0
XREAD_COUNT = 100
room_name = "global"


async def add_user(pool):
    added = await pool.sadd(room_name + ":user", 'a')
    if not added:
        await pool.srem(room_name + ":user", "a")
        added = await pool.sadd(room_name + ":user", 'a')
    return added


async def get_redis_pool():
    try:
        pool = await aioredis.create_redis_pool(
            (REDIS_HOST, REDIS_PORT), encoding='utf-8')
        return pool
    except ConnectionRefusedError as e:
        print('cannot connect to redis on:', REDIS_HOST, REDIS_PORT)
        return None


@router.post("/{board_id}/send")
async def send_message(
    board_id: int,
    data: MessageSchema,
    user: User = Depends(get_current_user_or_anonymous),
    db: Session = Depends(get_db)
):
    message, board, member = create_message(board_id, user, data, db)
    data_to_send = build_chat_message(message, board, member)
    pool = await get_redis_pool()
    await pool.xadd(
        stream=room_name,
        fields=data_to_send,
        message_id=b'*',
    )
    return data_to_send


@router.websocket("/ws")
async def board_chat(websocket: WebSocket):
    await websocket.accept()
    pool = await get_redis_pool()
    added = await add_user(pool)
    print(added)

    ws_connected = True
    while pool and ws_connected:
        try:
            events = await pool.xread(
                streams=[room_name],
                count=XREAD_COUNT,
                timeout=XREAD_TIMEOUT,
            )
            for _, e_id, event in events:
                event['e_id'] = e_id
                await websocket.send_json(event)
        except ConnectionClosedError:
            ws_connected = False

        except ConnectionClosedOK:
            ws_connected = False

        except ServerConnectionClosedError:
            print('redis server connection closed')
            return

        except Exception as e:
            print("Exception: ", e)
            raise e
    pool.close()
