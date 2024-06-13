# Лабораторная 2

## Задание 1

### Thread

```python
import threading
import time

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def calculate_sum():
    total_threads = 4
    total_sum = 0
    n = 1000000
    thread_list = []
    result = [0] * total_threads
    step = n // total_threads

    for i in range(total_threads):
        start = i * step + 1
        end = (i + 1) * step if i != total_threads - 1 else n
        thread = threading.Thread(target=calculate_partial_sum, args=(start, end, result, i))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    total_sum = sum(result)
    return total_sum

start_time = time.time()
sum_result = calculate_sum()
end_time = time.time()
print(f"Threading sum: {sum_result}, Time taken: {end_time - start_time} seconds")

```

### Multiprocess

```python

import multiprocessing
import time

def calculate_partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def calculate_sum():
    total_processes = 4
    total_sum = 0
    n = 1000000
    process_list = []
    manager = multiprocessing.Manager()
    result = manager.list([0] * total_processes)
    step = n // total_processes

    for i in range(total_processes):
        start = i * step + 1
        end = (i + 1) * step if i != total_processes - 1 else n
        process = multiprocessing.Process(target=calculate_partial_sum, args=(start, end, result, i))
        process_list.append(process)
        process.start()

    for process in process_list:
        process.join()

    total_sum = sum(result)
    return total_sum


if __name__ == '__main__':
    start_time = time.time()
    sum_result = calculate_sum()
    end_time = time.time()
    print(f"Multiprocessing sum: {sum_result}, Time taken: {end_time - start_time} seconds")

```


### Async

```python
import asyncio
import time

async def calculate_partial_sum(start, end):
    return sum(range(start, end + 1))

async def calculate_sum():
    total_tasks = 4
    n = 1000000
    step = n // total_tasks
    tasks = []

    for i in range(total_tasks):
        start = i * step + 1
        end = (i + 1) * step if i != total_tasks - 1 else n
        tasks.append(asyncio.create_task(calculate_partial_sum(start, end)))

    results = await asyncio.gather(*tasks)
    total_sum = sum(results)
    return total_sum

start_time = time.time()
sum_result = asyncio.run(calculate_sum())
end_time = time.time()
print(f"Async sum: {sum_result}, Time taken: {end_time - start_time} seconds")

```




## Задание 2


### Async

```python
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
```

### Thread

```python
from threading import Thread
import requests
from bs4 import BeautifulSoup
import time
from ex_2.urls import urls
from ex_2.db import save_to_database
from dotenv import load_dotenv

load_dotenv()


def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    save_to_database(url, title, 'threading')


def main(urls):

    threads = []
    for url in urls:
        thread = Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    with open('../times.txt', 'a') as f:
        f.write(f"Tread: {execution_time}\n")
```

### Multiprocess

```python
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup
import time
from ex_2.urls import urls
from ex_2.db import save_to_database
from dotenv import load_dotenv

load_dotenv()

def parse_and_save(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    save_to_database(url, title, 'mltprcs')
def main(urls):
    num_process = len(urls) if len(urls) < 4 else 4
    pool = Pool(processes=num_process)
    pool.map(parse_and_save, urls)


if __name__ == "__main__":
    start_time = time.time()
    main(urls)
    end_time = time.time()
    execution_time = end_time - start_time

    with open('../times.txt', 'a') as f:
        f.write(f"Multiprocess: {execution_time}\n")
```


### Database save (for threading and myltiprocess)

```python
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def save_to_database(url, title, method):
    
    
    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()
    curs.execute("INSERT INTO parce (url, title, process_type) VALUES (%s, %s, %s)",
                 (url, title, method))
    conn.commit()
    curs.close()
    conn.close()
```


## Результаты

    | Solution      | Time (seconds)     |
    |---------------|--------------------|
    | Async         | 1.2993099689483643 |
    | Multiprocess  | 1.6727426052093506 |
    | Threading     | 1.244816780090332  |

