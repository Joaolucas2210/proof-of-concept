import psycopg2
from src.config import Config
import logging

# Configuração do logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class BaseRepository:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                dbname=Config.DB_NAME
            )
            self.connection.autocommit = True
            logger.info("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def __del__(self):
        if self.connection:
            self.connection.close()
            logger.info("Conexão com o banco de dados fechada.")