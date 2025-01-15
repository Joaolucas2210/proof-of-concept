# import os
# import pytest
# import psycopg2
# from src.config import TestConfig
# from src.repository.base_repository import BaseRepository
# from src.repository.result_repository import ResultRepository
# from src.models.result_model import ResultModel

# @pytest.fixture(scope="session")
# def db_connection():
#     conn = psycopg2.connect(
#         host=TestConfig.DB_HOST,
#         port=TestConfig.DB_PORT,
#         user=TestConfig.DB_USER,
#         password=TestConfig.DB_PASSWORD
#     )
#     yield conn
#     conn.close()

# @pytest.fixture(scope="session")
# def test_db(db_connection):
#     with db_connection.cursor() as cursor:
#         cursor.execute(f"DROP DATABASE IF EXISTS {TestConfig.DB_NAME}")
#         cursor.execute(f"CREATE DATABASE {TestConfig.DB_NAME}")
#     db_connection.commit()

#     yield TestConfig.DB_NAME

#     with db_connection.cursor() as cursor:
#         cursor.execute(f"DROP DATABASE {TestConfig.DB_NAME}")
#     db_connection.commit()

# @pytest.fixture
# def repository(test_db):
#     repo = ResultRepository()
#     repo.create_table()
#     yield repo
#     with repo.connection.cursor() as cursor:
#         cursor.execute("DROP TABLE IF EXISTS resultados")
#     repo.connection.commit()