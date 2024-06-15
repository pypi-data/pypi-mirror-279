#!/usr/bin/python3
# -*- encoding=utf8 -*-

import requests

from nio import AsyncClient, AsyncClientConfig

from auth import login


class ChatsClient(AsyncClient):

    def __init__(self, user_name: str = '', password: str = '', auth_token: str = ''):
        if not auth_token:
            auth_token = login(user_name, password)

        client_config = AsyncClientConfig(custom_headers={'authorization': f'Bearer {auth_token}'})

        res = requests.get(f'https://www.reddit.com/user/{user_name}/about.json')
        data = res.json().get('data', {})
        user_id = f"t2_{data.get('id')}"

        super().__init__('https://matrix.redditspace.com', f'@{user_id}:reddit.com', config=client_config)
        self.access_token = ''
