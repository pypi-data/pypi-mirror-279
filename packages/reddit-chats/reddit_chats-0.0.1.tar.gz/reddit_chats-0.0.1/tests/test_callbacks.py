#!/usr/bin/python3
# -*- encoding=utf8 -*-

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
                f'{room.user_name(event.sender)} | {event}'
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
    client = ChatsClient(user_name='free_user0007', password='')

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
