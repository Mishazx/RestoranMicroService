import logging
import time
import psycopg2
from database import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

logger = logging.getLogger('DBCheck')

def wait_for_db(max_retries=30, delay=2):
    """
    Ждет, пока база данных станет доступной
    
    Args:
        max_retries (int): Максимальное количество попыток
        delay (int): Задержка между попытками в секундах
    """
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.close()
            logger.info("Successfully connected to the database")
            return True
        except psycopg2.OperationalError as e:
            logger.warning(f"Database connection attempt {i + 1}/{max_retries} failed: {str(e)}")
            time.sleep(delay)
    
    raise Exception("Could not connect to the database after multiple attempts") 