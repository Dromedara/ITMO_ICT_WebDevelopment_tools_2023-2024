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