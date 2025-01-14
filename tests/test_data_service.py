import pytest
import pandas as pd
from src.services.data_service import DataService
from src.repository.result_repository import ResultRepository
from src.models.result_model import ResultModel

def test_save_cross_tabs(repository):
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

    with repository.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM resultados")
        results = cursor.fetchall()
    assert len(results) == 6  # 2 * 3 = 6 registros esperados