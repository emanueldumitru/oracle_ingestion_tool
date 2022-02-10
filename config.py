import os
import cx_Oracle
import sqlite3
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Here we will use common configuration variables between environments
    pass

class DevelopmentConfig(Config):
    MODE = "development"
    ORACLE_HOST = "localhost"
    ORACLE_PORT = 1521
    ORACLE_SID = "xe"
    ORACLE_USER = "test"
    ORACLE_PASS = "passtest"
    DEBUG = True
    SQL_QUERY = "SELECT ID, C FROM CLOB_TBL"
    CLOB_DATA_FILE_PATH = f"{basedir}/input/example.txt"
    PARQUET_OUTPUT_FILE_PATH = f"{basedir}/output/clob.parquet"

    @staticmethod
    def create_connection():
        dsn_tns = cx_Oracle.makedsn(DevelopmentConfig.ORACLE_HOST, DevelopmentConfig.ORACLE_PORT, DevelopmentConfig.ORACLE_SID)
        connection = cx_Oracle.connect(user=DevelopmentConfig.ORACLE_USER,
                                       password=DevelopmentConfig.ORACLE_PASS,
                                       dsn=dsn_tns)
        return connection


class TestingConfig(Config):
    MODE = "testing"
    CLOB_DATA_FILE_PATH = f"{basedir}/input/example_test.txt"
    PARQUET_OUTPUT_FILE_PATH = f"{basedir}/output/clob_test.parquet"
    TESTING = True
    TEST_SQL_QUERY = "SELECT ID, C FROM CLOB_TBL"
    TEST_CLOB = "PLorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."


    @staticmethod
    def create_connection():
        connection = sqlite3.connect(f'{basedir}/input/test.db')
        return connection


class ProductionConfig(Config):
    MODE = "production"

config = {
    'development': DevelopmentConfig,
    'testing'    : TestingConfig,
    'production' : ProductionConfig,
    'default'    : DevelopmentConfig
}