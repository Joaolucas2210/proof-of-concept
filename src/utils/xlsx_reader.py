import os
import pandas as pd
import logging
from typing import List

# Configuração do logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class ExcelReader:
    def __init__(self, filename: str, header_skip: int = 5):
        self.filename = filename
        self.header_skip = header_skip
        self.df = pd.DataFrame()

    def get_file_path(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"Diretório atual: {current_dir}")
        base_dir = os.path.dirname(os.path.dirname(current_dir))
        logger.info(f"Diretório base: {base_dir}")
        file_path = os.path.join(base_dir, "data", self.filename)
        logger.info(f"Caminho do arquivo: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        return file_path

    def read_excel(self):
        file_path = self.get_file_path()
        try:
            # Ler todas as colunas como strings para evitar problemas de formatação
            self.df = pd.read_excel(file_path, header=self.header_skip, dtype=str, engine='openpyxl')
            logger.info("Arquivo Excel lido com sucesso.")
            logger.debug(f"Colunas originais do DataFrame: {self.df.columns.tolist()}")

            # Converter todos os nomes das colunas para strings, remover espaços e converter para minúsculas
            self.df.columns = self.df.columns.map(str).str.strip().str.lower()
            logger.debug(f"Colunas após conversão para string e normalização: {self.df.columns.tolist()}")
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo Excel: {e}")
            raise

    def process_year_columns(self) -> List[str]:
        # Identificar colunas que representam anos (apenas dígitos e com comprimento 4)
        year_columns = [col for col in self.df.columns if col.isdigit() and len(col) == 4]
        if not year_columns:
            logger.error("Nenhuma coluna de ano foi identificada. Verifique o arquivo Excel.")
            raise ValueError("Nenhuma coluna de ano foi identificada. Verifique o arquivo Excel.")
        logger.info(f"Colunas de anos identificadas: {year_columns}")

        # Converter as colunas de anos para numérico e somar
        for ano in year_columns:
            try:
                # Remover pontos e vírgulas, se presentes, e converter para inteiro
                self.df[ano] = self.df[ano].str.replace('.', '', regex=False).str.replace(',', '', regex=False).str.strip()
                self.df[ano] = pd.to_numeric(self.df[ano], errors='coerce').fillna(0).astype(int)
            except Exception as e:
                logger.error(f"Erro ao processar a coluna {ano}: {e}")
                raise

        # Adicionar a coluna 'total_anos' somando todos os anos
        self.df['total_anos'] = self.df[year_columns].sum(axis=1)

        return year_columns

    def select_required_columns(self, required_columns: List[str]):
        # Normalizar os nomes das colunas necessárias
        required_columns = [col.lower().strip() for col in required_columns]
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            logger.error(f"Colunas faltando no DataFrame: {missing_columns}")
            raise KeyError(f"Colunas faltando no DataFrame: {missing_columns}")
        self.df = self.df[required_columns]
        logger.info(f"DataFrame com colunas selecionadas: {self.df.columns.tolist()}")

    def cross_tabulations(self):
        # Verifica se as colunas necessárias existem
        required = ['sexo', 'local', 'idade', 'total_anos']
        for col in required:
            if col not in self.df.columns:
                logger.error(f"Coluna necessária para cruzamento não encontrada: {col}")
                raise KeyError(f"Coluna necessária para cruzamento não encontrada: {col}")

        # Cruzamento Sexo x Local
        sexo_local = pd.pivot_table(
            self.df,
            values='total_anos',
            index='sexo',
            columns='local',
            aggfunc='sum',
            fill_value=0
        )
        logger.info("Cruzamento Sexo x Local realizado com sucesso.")

        # Cruzamento Local x Idade
        local_idade = pd.pivot_table(
            self.df,
            values='total_anos',
            index='local',
            columns='idade',
            aggfunc='sum',
            fill_value=0
        )
        logger.info("Cruzamento Local x Idade realizado com sucesso.")

        # Cruzamento Sexo x Idade
        sexo_idade = pd.pivot_table(
            self.df,
            values='total_anos',
            index='sexo',
            columns='idade',
            aggfunc='sum',
            fill_value=0
        )
        logger.info("Cruzamento Sexo x Idade realizado com sucesso.")

        return {
            'sexo_x_local': sexo_local,
            'local_x_idade': local_idade,
            'sexo_x_idade': sexo_idade
        }

    def run(self):
        self.read_excel()
        year_columns = self.process_year_columns()
        required_columns = ['sexo', 'local', 'idade', 'total_anos']
        self.select_required_columns(required_columns)
        cross_tabs = self.cross_tabulations()
        return cross_tabs