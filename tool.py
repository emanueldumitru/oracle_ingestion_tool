import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import cx_Oracle
from config import config
import os

basedir = os.path.abspath(os.path.dirname(__file__))
cx_Oracle.init_oracle_client(lib_dir=f"{basedir}/oracle_client/instantclient_19_8")


class IngestionTool:
    def __init__(self, config_name):
        conf = config[config_name]
        print(f">>> Running in {conf.MODE} mode")

        self.config = conf
        self.connection = conf.create_connection()

    def insert_data_to_oracle_db(self):
        try:
            with open(self.config.CLOB_DATA_FILE_PATH, 'r') as f:
                text_data = f.read()

            cursor = self.connection.cursor()
            cursor.execute("""INSERT INTO CLOB_TBL(C) VALUES (:clobdata)""", {
                                    "clobdata": text_data
                                })
            self.connection.commit()

        except cx_Oracle.Error as error:
            print("Error occurred: ", error)


    def from_oracle_db_to_pa_table(self):
        try:
            select_sql = self.config.SQL_QUERY
            df = pd.read_sql(select_sql, con=self.connection)
            df['C'] = df['C'].apply(lambda x: x.read())
            table = pa.Table.from_pandas(df)
            return table
        except cx_Oracle.Error as error:
            print("Error occurred: ", error)
            return None


    def pa_table_to_parquet_file(self):
        try:
            outputfile = self.config.PARQUET_OUTPUT_FILE_PATH
            table = self.from_oracle_db_to_pa_table()
            with pq.ParquetWriter(outputfile, schema=table.schema
                    , use_deprecated_int96_timestamps=True
                    , allow_truncated_timestamps=True
                                  ) as parquet_writer:
                parquet_writer.write_table(table)
        except Exception as err:
            print(err)


    def close_connection(self):
        self.connection.close()

def main():
    tool = IngestionTool('default')
    tool.insert_data_to_oracle_db()
    tool.pa_table_to_parquet_file()
    tool.close_connection()


if __name__ == "__main__":
    main()
