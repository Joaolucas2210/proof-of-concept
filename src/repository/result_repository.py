from psycopg2 import extras
from typing import List
from src.models.result_model import ResultModel
from src.repository.base_repository import BaseRepository
import logging

# Configuração do logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class ResultRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS resultados (
            id SERIAL PRIMARY KEY,
            tipo_cruzamento VARCHAR(50),
            chave1 VARCHAR(100),
            chave2 VARCHAR(100),
            total_anos BIGINT
        );
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            logger.info("Tabela 'resultados' garantida no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao criar tabela 'resultados': {e}")
            raise

    def insert_result(self, result: ResultModel):
        query = """
        INSERT INTO resultados (tipo_cruzamento, chave1, chave2, total_anos)
        VALUES (%s, %s, %s, %s);
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (result.tipo_cruzamento, result.chave1, result.chave2, result.total_anos))
            logger.debug(f"Registro inserido: {result}")
        except Exception as e:
            logger.error(f"Erro ao inserir registro: {e}")
            raise

    def insert_results(self, results: List[ResultModel]):
        if not results:
            logger.warning("Nenhum registro para inserir.")
            return
        query = """
        INSERT INTO resultados (tipo_cruzamento, chave1, chave2, total_anos)
        VALUES %s;
        """
        values = [(r.tipo_cruzamento, r.chave1, r.chave2, r.total_anos) for r in results]
        try:
            with self.connection.cursor() as cursor:
                extras.execute_values(
                    cursor, query, values, template=None, page_size=100
                )
            logger.debug(f"{len(results)} registros inseridos em lote.")
        except Exception as e:
            logger.error(f"Erro ao inserir registros em lote: {e}")
            raise