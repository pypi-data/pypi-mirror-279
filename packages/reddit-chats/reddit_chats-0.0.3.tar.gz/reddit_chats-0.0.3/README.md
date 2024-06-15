# Reddit Chats SDK

reddit_chats provides SDK for Chat Bots at Reddit. This is non-official python library for Reddit Chats Bots.

### How To Install

You can install the package with pip:
```bash
pip install reddit_chats
```

### Examples

Here are several simple examples of how you can create chat bots using reddit_chats library. Please note, reddit_chats 
library is compatible with [matrix-nio](https://github.com/matrix-nio/matrix-nio) python library, and provides the 
same SDK as AsyncClient from [matrix-nio](https://github.com/matrix-nio/matrix-nio).

#### Join chat room and send message

```python
import asyncio
from reddit_chats import ChatsClient


async def run() -> None:
    # example of the room id, it should contain ":reddit.com" 
    # and it should be a real chat room id
    my_chat_room = '!4HMffHQivx4w7SWY_ckoxLbQs_-Ku3f1YX9b00-Ny-E:reddit.com'

    client = ChatsClient(user_name='my_reddit_user', password='my_password')

    # This is how bot can join chat room by it's id:
    await client.join(my_chat_room)

    # This is how to send new text message to the chat room
    await client.room_send(
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
```

#### Create group chat and invite users there

```python
import asyncio
from reddit_chats import ChatsClient


async def run() -> None:
    client = ChatsClient(user_name='my_reddit_user', password='my_password')

    # This is how bot can create group chat rooms and invite users there
    room = await client.room_create(
        name='My Group Chat Room',
        is_direct=False,  # direct rooms are 1:1 chats between users
        federate=False,
        invite=('@t2_innwi:reddit.com',)
    )
    print("Chat Room id:", room.room_id)

    # This is how bot can invite another user to the chat room
    await client.room_invite(user_id='t2_innwi', room_id=room.room_id)

    # This is how to send new text message to the chat room
    await client.room_send(
        # room id should be with ":reddit.com"
        room_id=room.room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": "Hello world!"
        }
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run())
```

#### Example of the bot that listens to all new messages and reactions

In this example the bot will initialize two callback functions and will listen for all new chat messages and all new reactions (in all rooms that user joined).

```python
import asyncio
import functools

from nio import MatrixRoom, RoomMessageText, Event
from reddit_chats import ChatsClient


async def reaction_callback(client: ChatsClient, room: MatrixRoom, event: Event) -> None:
    """ This function will be triggered on every new reaction in all rooms that bot joined. """

    try:
        if 'm.relates_to' in event.source['content']:
            reaction = event.source['content']['m.relates_to'].get('key')
            event_id = event.source['content']['m.relates_to'].get('event_id')

            print(
                f'Reaction received in room {room.display_name}\n'
                f'{room.user_name(event.sender)} | {event}\n'
                f'{reaction} {event_id}'
            )
    except:
        pass  # just ignore any errors to make sure the bot will not stop


async def message_callback(client: ChatsClient, room: MatrixRoom, event: RoomMessageText) -> None:
    """ This function will be triggered on every new message in all rooms that bot joined. """

    try:
        print(
            f"Message received in room {room.display_name}\n"
            f"{room.user_name(event.sender)} | {event}"
        )
    except:
        pass  # just ignore any errors to make sure the bot will not stop


async def run() -> None:
    client = ChatsClient(user_name='my_reddit_user', password='my_password')

    # Create callback for new messages in chats:
    callback = functools.partial(message_callback, client)
    client.add_event_callback(callback, RoomMessageText)

    # Create callback for all events types (including UnknownEvent)
    callback = functools.partial(reaction_callback, client)
    client.add_event_callback(callback, Event)

    await client.sync_forever(timeout=10000)  # milliseconds


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run())
```

#### Bot that welcomes everyone who joins the room
```python
import asyncio
import functools

from nio import MatrixRoom, RoomMemberEvent
from reddit_chats import ChatsClient


# Make sure the bot only works in this room
my_room_id = '!4HMffHQivx4w7SWY_ckoxLbQs_-Ku3f1YX9b00-Ny-E:reddit.com'


async def intro(client: ChatsClient) -> None:
    """ This function will be triggered once every time you start the bot. """

    await client.room_send(
        room_id=my_room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": """Hi there, I'm a bot who greets everybody who joins the chat!"""
        }
    )

    
async def join_callback(client: ChatsClient, room: MatrixRoom, event: RoomMemberEvent) -> None:
    """ This function will be triggered every time a new user joins the chat room. """

    try:
        if room.room_id == my_room_id:
            if event.content['membership'] == 'join':
                await client.room_send(
                    room_id=room.room_id,
                    message_type="m.room.message",
                    content={
                        "msgtype": "m.text",
                        "body": f"""@{room.user_name(event.sender)} joined. Welcome to the chat!"""
                    }
                )
    except:
        pass  # just ignore any errors to make sure the bot will not stop


async def run() -> None:
    client = ChatsClient(user_name='my_reddit_user', password='my_password')

    # Create callback for join event:
    callback = functools.partial(join_callback, client)
    client.add_event_callback(callback, RoomMemberEvent)

    await intro(client)
    await client.sync_forever(timeout=10000)  # milliseconds


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    loop.run_until_complete(run())
```