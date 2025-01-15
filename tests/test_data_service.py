import pytest
from unittest.mock import patch
import pandas as pd
from src.services.data_service import DataService
from src.repository.result_repository import ResultRepository
from src.models.result_model import ResultModel


class FakeConnection:
    def __init__(self):
        self.autocommit = False

    def close(self):
        print("Fechando FakeConnection")

    def cursor(self):
        return FakeCursor()
class FakeCursor:
    def __init__(self):
        self.fetchall_data = []

    def execute(self, query):
        print(f"Executando consulta: {query}")

    def fetchall(self):
        return self.fetchall_data

    def close(self):
        print("Fechando FakeCursor")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()



@patch('psycopg2.connect')
@patch('src.repository.result_repository.ResultRepository.insert_results')
def test_save_cross_tabs(insert_results,connect):
    insert_results.return_value = None
    connect.return_value = FakeConnection()
    repository = ResultRepository()
    data_service = DataService(repository)
    cross_tabs = {
        'sexo_x_local': pd.DataFrame({
            'Masculino': {'SP': 450, 'RJ': 550},
            'Feminino': {'SP': 750, 'RJ': 850}
        }),
        'local_x_idade': pd.DataFrame({
            '25': {'SP': 100, 'RJ': 150},
            '30': {'SP': 200, 'RJ': 250}
        }),
        'sexo_x_idade': pd.DataFrame({
            '25': {'Masculino': 100, 'Feminino': 200},
            '30': {'Masculino': 150, 'Feminino': 250}
        })
    }
    data_service.save_cross_tabs(cross_tabs)
