import psycopg2
from config import host, database, user, password, port

def get_connection():
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn
    except Exception as error:
        print(f"Ошибка подключения: {error}")
        return None