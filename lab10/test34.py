import psycopg2
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    conn = psycopg2.connect(
        host="localhost",
        dbname="lab10",
        user="postgres",
        password="Almaty250505",
        port=5432,
        client_encoding='utf8'
    )
    print("Connected successfully.")
except Exception as e:
    print(f"Error: {e}")
