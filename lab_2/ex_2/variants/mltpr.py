import os
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