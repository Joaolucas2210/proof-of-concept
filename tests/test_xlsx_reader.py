import pandas as pd
import pytest
from src.utils.xlsx_reader import ExcelReader

@pytest.fixture
def sample_excel_file(tmp_path):
    data = {
        'Sexo': ['Masculino', 'Feminino', 'Masculino', 'Feminino'],
        'Local': ['SP', 'RJ', 'MG', 'SP'],
        'Idade': [25, 30, 35, 40],
        '2020': [100, 200, 150, 250],
        '2021': [150, 250, 200, 300],
        '2022': [200, 300, 250, 350]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample.xlsx"
    with pd.ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=False, startrow=5)
    return file_path  

def test_read_excel(sample_excel_file):
    reader = ExcelReader(sample_excel_file)
    reader.read_excel()
    assert not reader.df.empty
    assert set(reader.df.columns) == {'sexo', 'local', 'idade', '2020', '2021', '2022'}

def test_process_year_columns(sample_excel_file):
    reader = ExcelReader(sample_excel_file)
    reader.read_excel()
    year_columns = reader.process_year_columns()
    assert year_columns == ['2020', '2021', '2022']
    assert 'total_anos' in reader.df.columns

def test_select_required_columns(sample_excel_file):
    reader = ExcelReader(sample_excel_file)
    reader.read_excel()
    reader.process_year_columns()
    reader.select_required_columns(['sexo', 'local', 'idade', 'total_anos'])
    assert set(reader.df.columns) == {'sexo', 'local', 'idade', 'total_anos'}

def test_cross_tabulations(sample_excel_file):
    reader = ExcelReader(sample_excel_file)
    cross_tabs = reader.run()
    assert 'sexo_x_local' in cross_tabs
    assert 'local_x_idade' in cross_tabs
    assert 'sexo_x_idade' in cross_tabs
