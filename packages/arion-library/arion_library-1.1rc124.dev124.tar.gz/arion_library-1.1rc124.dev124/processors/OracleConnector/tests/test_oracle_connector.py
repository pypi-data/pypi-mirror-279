import pytest
from ..lib.OracleDatabase import OracleDatabase  # Importez votre classe OracleDatabase
import logging

@pytest.fixture
def oracle_database_client():
    user = "system"
    password = "oracle"
    dsn = "localhost:1521/oracle"
    yield OracleDatabase(user, password, dsn)

def test_connect(oracle_database_client):
    assert oracle_database_client.connection is not None

def test_insert_and_query_data(oracle_database_client):
    # Définissez vos données de test ici
    
    truncate_query = "TRUNCATE TABLE test"
    
    table = oracle_database_client.execute_query(truncate_query)

    test_data = [
        {"column1": 5, "column2": 87},
        {"column1": 65, "column2": 35}
    ]

    # Insérez les données de test dans la base de données
    errors = oracle_database_client.insert_data("test", test_data)

    # Vérifiez s'il y a des erreurs lors de l'insertion
    assert not errors

    # Interrogez les données insérées pour vérifier qu'elles sont correctes
    query_result = oracle_database_client.select_data("SELECT * FROM test")
    print(query_result)

    # Vérifiez que les données sont correctes
    assert len(query_result) == len(test_data)
    assert query_result[0][1] == 5
    assert query_result[0][2] == 87
    assert query_result[1][1] == 65
    assert query_result[1][2] == 35

    

def test_close_connection(oracle_database_client):
    oracle_database_client.close_connection()
    assert oracle_database_client.connection is None  # Vérifiez que la connexion est fermée
