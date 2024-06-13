import os
from threading import Thread
import requests
from bs4 import BeautifulSoup
import psycopg2
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