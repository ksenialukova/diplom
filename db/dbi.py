from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pathlib import Path


def get_db_connection_string(creds):
    return f'postgresql://{creds["user"]}:{creds["password"]}@{creds["host"]}:{creds["port"]}/{creds["database"]}'


def get_db_credentials():
    return {
        "host": '',
        "port": '',
        "database": '',
        "user": '',
        "password": ''
    }


def get_db_connection_str():
    creds = get_db_credentials()
    return get_db_connection_string(creds)


class DiplomDB:
    def __init__(
            self,
            connectable
    ):
        """
        Use SQLAlchemy Connectable to perform ACE queries.
        """
        self.connectable = connectable

    def fill_cash_entities(self):
        df = pd.read_csv('../data/cash_entities/cash_entities.csv',
                         dtype={
                             'X_COORD': np.str,
                             'Y_COORD': np.str
                         })
        with self.connectable.connect() as conn:
            for index, row in df.iterrows():
                sql = (
                    f'''
                    INSERT INTO cash_entity (
                    CE_CODE,
                    CE_NAME,
                    CE_TYPE,
                    PARENT_CODE,
                    X_COORD,
                    Y_COORD
                    ) VALUES (
                        {row['CODE']},
                        '{row['NAME']}',
                        '{row['TYPE']}',
                        {row['PARENT_CODE']},
                        '{row['X_COORD']}',
                        '{row['Y_COORD']}'
                        )'''
                )
                conn.execute(sql)

    def fill_all_balances(self):
        path = Path('../data/balances/')

        df = (
            pd.concat([
                pd.read_csv(f, dtype={'PERCENT': np.str})
                for f in path.glob("*")
            ]).sort_values(by=['DATE'])
        )

        with self.connectable.connect() as conn:
            for index, row in df.iterrows():
                sql = (
                    f'''
                    INSERT INTO balance (date, code, percent)
                    VALUES (
                    '{row['DATE']}',
                    '{row['CODE']}',
                    {row['PERCENT']}
                    )'''
                )
                conn.execute(sql)

    def return_shipments(self):
        sql = f'select * from shipments'

        df = pd.read_sql(sql, self.connectable)

        return df


engine = create_engine(get_db_connection_str())

db = DiplomDB(engine)
