import requests


def get_user_id(user_name: str) -> str:
    res = requests.get(f'https://www.reddit.com/user/{user_name}/about.json')
    data = res.json().get('data', {})
    user_id = f"t2_{data.get('id')}"

    return user_id
