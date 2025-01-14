import sys
import logging
from src.utils.xlsx_reader import ExcelReader
from src.services.data_service import DataService
from src.repository.result_repository import ResultRepository

# Configuração básica do logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    if len(sys.argv) < 2:
        logger.error("Uso: python src/main.py <arquivo.xlsx>")
        sys.exit(1)

    excel_filename = sys.argv[1]
    reader = ExcelReader(excel_filename)
    try:
        cross_tabs = reader.run()
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except KeyError as e:
        logger.error(f"Erro no processamento dos dados: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado ao processar o arquivo: {e}")
        sys.exit(1)

    # Inicialize o repositório e o serviço de dados
    repository = ResultRepository()
    data_service = DataService(repository)

    # Salve os cruzamentos no banco de dados
    data_service.save_cross_tabs(cross_tabs)

    logger.info("Processamento concluído!")

if __name__ == "__main__":
    main()