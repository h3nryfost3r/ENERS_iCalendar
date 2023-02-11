from typing import List

import asyncio
import aiohttp
from fake_useragent import UserAgent


class ResponseHandler():
    __ENERS_API_URL = 'https://eners.kgeu.ru/apish2.php'
    __WEEK_EOF = 20

    __responses: List[str]

    def __init__(self, group_name: str):
        urls = list(map(
            lambda week: self.__ENERS_API_URL + f'?group={group_name}&week={week}&type=one',
            range(1, self.__WEEK_EOF)))
        asyncio.run(self.__load_data_responses(urls))

    async def __get_week(self, session: aiohttp.ClientSession, url):
        async with session.get(url) as resp:
            http_body = await resp.text()
            return http_body

    async def __load_data_responses(self, urls):
        headers = {
            "User-Agent": UserAgent(use_external_data=True).random
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            for url in urls:
                tasks.append(
                    asyncio.ensure_future(self.__get_week(session, url)))

            responses = await asyncio.gather(*tasks)
            self.__responses = list(responses)

    def get_responses(self):
        return self.__responses
