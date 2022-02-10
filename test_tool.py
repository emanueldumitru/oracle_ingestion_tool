import pytest
import sqlite3
from tool import IngestionTool

ingestion_tool = IngestionTool("testing")

@pytest.fixture(scope="session", autouse=True)
def manage_test_context():
       with open('setup_test_context.sql', 'r') as sql_file:
              sql_script = sql_file.read()

       connection = sqlite3.connect('input/test.db')
       cursor = connection.cursor()
       cursor.executescript(sql_script)
       connection.close()
       yield

def test_insert_data_to_oracle_db():
       # Run code
       ingestion_tool.insert_data_to_oracle_db()

       # Test setup
       connection = sqlite3.connect('input/test.db')
       cursor = connection.cursor()
       cursor.execute(ingestion_tool.config.TEST_SQL_QUERY)
       data = cursor.fetchall()

       # Asserts
       assert len(data) > 0
       assert data[0][1] == ingestion_tool.config.TEST_CLOB



