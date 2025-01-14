import logging
from typing import Dict
from src.repository.result_repository import ResultRepository
from src.models.result_model import ResultModel
import pandas as pd

# Configuração do logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class DataService:
    def __init__(self, repository: ResultRepository):
        self.repo = repository

    def save_cross_tabs(self, cross_tabs: Dict[str, pd.DataFrame]):
        for tipo_cruzamento, df in cross_tabs.items():
            logger.info(f"Iniciando inserção dos resultados para '{tipo_cruzamento}'")
            results = []
            for chave1, row in df.iterrows():
                for chave2, total in row.items():
                    result = ResultModel(
                        tipo_cruzamento=tipo_cruzamento,
                        chave1=str(chave1),
                        chave2=str(chave2),
                        total_anos=int(total)
                    )
                    results.append(result)
            logger.debug(f"Total de registros a serem inseridos para '{tipo_cruzamento}': {len(results)}")
            # Inserir em lotes para eficiência
            try:
                self.repo.insert_results(results)
                logger.info(f"Cruzamento '{tipo_cruzamento}' salvo com sucesso.")
            except Exception as e:
                logger.error(f"Erro ao salvar o cruzamento '{tipo_cruzamento}': {e}")
                raise