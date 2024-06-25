import logging
import requests
from fake_useragent import UserAgent


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

useragent = UserAgent()


def generate_random_ua():
    return useragent.random


def get(url: str, headers: dict = None, **kwargs):
    if not headers:
        headers = {}
    headers['User-Agent'] = generate_random_ua()
    try:
        resp = requests.get(url, headers=headers, **kwargs)
        return resp
    except Exception as e:
        logging.error(f"Error Requesting {url}: {e}")
        return None
