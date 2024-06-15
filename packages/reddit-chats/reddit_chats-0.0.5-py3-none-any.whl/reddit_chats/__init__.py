#!/usr/bin/python3
# -*- encoding=utf8 -*-

import requests

from nio import AsyncClient, AsyncClientConfig

from reddit_chats.auth import login
from reddit_chats.api import get_user_id


class ChatsClient(AsyncClient):

    def __init__(self, user_name: str = '', password: str = '', auth_token: str = ''):
        if not auth_token:
            auth_token = login(user_name, password)

        client_config = AsyncClientConfig(custom_headers={'authorization': f'Bearer {auth_token}'})

        user_id = get_user_id(user_name)

        super().__init__('https://matrix.redditspace.com', user_id, config=client_config)
        self.access_token = auth_token
