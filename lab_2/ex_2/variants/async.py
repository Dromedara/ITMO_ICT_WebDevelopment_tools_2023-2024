import os

import aiohttp
import asyncio
import asyncpg
from bs4 import BeautifulSoup
import time
from ex_2.urls import urls
from dotenv import load_dotenv

load_dotenv()


async def save_to_db(data):
    conn = await asyncpg.connect(os.getenv("DB_URL"))
    try:
        await conn.execute(
            "INSERT INTO parce (url, title, process_type) VALUES ($1, $2, $3)",
            data['url'],  data['title'], 'async'
        )
    finally:
        await conn.close()


async def parse_and_save(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text
        await save_to_db({'url': url, 'title': title})


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(parse_and_save(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main(urls))
    end_time = time.time()
    execution_time = end_time - start_time
    with open('../times.txt', 'a') as f:
        f.write(f"Async: {execution_time}\n")