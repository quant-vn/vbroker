import time
import requests


class RequestHandler:
    def __init__(self) -> None:
        self.__timeout: int = 10

    def get(self, url: str, headers: dict, params: dict, limit: int = 0) -> dict:
        try:
            print(f"[vBroker] Call ~> GET: {url}: {params}")
            res = requests.get(url, headers=headers, params=params, timeout=self.__timeout)
            if limit:
                time.sleep(limit)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            raise e

    def post(self, url: str, headers: dict, data: dict = {}, limit: int = 0) -> dict:
        try:
            print(f"[vBroker] Call ~> POST: {url} data: {data}")
            if data:
                res = requests.post(url, headers=headers, json=data, timeout=self.__timeout)
            else:
                res = requests.post(url, headers=headers, timeout=self.__timeout)
            if limit:
                time.sleep(limit)
            res.raise_for_status()
            return res.json()
        except requests.RequestException as e:
            raise e


request_handler = RequestHandler()
