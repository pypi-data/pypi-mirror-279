#!/usr/bin/python3
# -*- encoding=utf8 -*-

import json
import time
import uuid

import requests
from latest_user_agents import get_random_user_agent


def get_reddit_access_token(username: str, password: str) -> str:
    """ This function obtains Reddit API auth token in a little hacky way. """

    # Please note - the user agent should be up-to-date, or we will get broken token
    user_agent = get_random_user_agent()

    url = f"https://old.reddit.com/api/login/{username}"

    data = {
        "op": "login",
        "dest": "https://old.reddit.com/",
        "user": username,
        "passwd": password,
        "api_type": "json",
    }

    headers = {
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    res = requests.post(url, data=data, headers=headers, timeout=100)

    res = requests.get(
        'https://chat.reddit.com/',
        headers={'user-agent': user_agent},
        cookies=res.cookies,
        timeout=100,
    )

    token = ''
    if '{&quot;token&quot;:&quot;' in res.content.decode('utf-8'):
        s = res.content.decode('utf-8').split('{&quot;token&quot;:&quot;')

        token = s[1].split('&quot;')[0]

    if not token:
        raise Exception(f'Authorization failed...')

    return f'Bearer {token}'


def login(username: str, password: str) -> str:
    """ We need to use Reddit API token as a custom token for authorization in matrix. """

    reddit_token = get_reddit_access_token(username=username, password=password)
    matrix_url = 'https://matrix.redditspace.com/_matrix/client/v3/login'

    matrix_token = reddit_token
    if 'Bearer' in reddit_token:
        matrix_token = reddit_token.split("Bearer ")[1]

    data = {
        "type": "com.reddit.token",
        "device_id": f"{uuid.uuid4()}",
        "token": matrix_token
    }

    headers = {
        "authorization": "",
    }

    time.sleep(0.1)

    res = requests.post(url=matrix_url, data=json.dumps(data), headers=headers)

    if 'token is invalid' in res.text:
        matrix_token = ''
        raise Exception(f'Failed to authorize: {res.text}')

    return matrix_token
