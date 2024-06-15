#!/usr/bin/python3
# -*- encoding=utf8 -*-

import asyncio

from reddit_chats import ChatsClient


async def run() -> None:

    my_chat_room = '!4HMffHQivx4w7SWY_ckoxLbQs_-Ku3f1YX9b00-Ny-E:reddit.com'

    client = ChatsClient(user_name='free_user0007', password='')

    # This is how bot can create group chat rooms and invite users there
    room = await client.room_create(
        name='My Group Chat Room',
        is_direct=False,  # direct rooms are 1:1 chats between users
        federate=False,
        invite=('@t2_innwi:reddit.com',)
    )
    print(room.room_id)

    # This is how bot can join chat room by it's id:
    await client.join(my_chat_room)

    # This is how bot can invite another user to the chat room
    await client.room_invite(user_id='t2_innwi', room_id=my_chat_room)

    # This is how to send new text message to the chat room
    await client.room_send(
        # room id should be with ":reddit.com"
        room_id=my_chat_room,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "Hello world!"
        }
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run())
