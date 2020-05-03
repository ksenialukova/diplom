from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from pathlib import Path


def get_db_connection_string(creds):
    return f'postgresql://{creds["user"]}:{creds["password"]}@{creds["host"]}:{creds["port"]}/{creds["database"]}'


def get_db_credentials():
    return {
        "host": 'localhost',
        "port": '5433',
        "database": 'postgres',
        "user": 'postgres',
        "password": 'postgres'
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
            ]).sort_values(by=['DATE', 'CODE'])
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

    def return_intensities_and_coords_by_date(self, current_date):
        sql = f'''
        select ce_type, x_coord, y_coord, percent
        from cash_entity
        join balance b on cash_entity.ce_code = b.code 
        where date= '{ current_date }'
        '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def fill_cost(self):
        df = pd.read_csv('../data/distances/distances.csv')
        with self.connectable.connect() as conn:
            for index, row in df.iterrows():
                sql = (
                    f'''
                            INSERT INTO cost (
                            FROM_CODE,
                            TO_CODE,
                            DISTANCE,
                            DURATION
                            ) VALUES (
                                {row['FROM_CODE']},
                                {row['TO_CODE']},
                                {row['DISTANCE']},
                                {row['DURATION']}
                                )'''
                )
                conn.execute(sql)

    def get_min_max_date(self):
        sql = f'''
                select min(date), max(date)
                from balance
                '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def get_atms(self):
        sql = f'''
                select ce_code
                from cash_entity
                where ce_type='A'
                '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def get_entities(self, depo):
        sql = f'''
                select *
                from cash_entity
                where parent_code = {depo}
                '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def get_balances(self):
        sql = f'''
                select *
                from balance
                '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def add_forecast_shipment(self,
                              ce_code,
                              last_shipment,
                              next_shipment,
                              days_for_filling
                              ):
        with self.connectable.connect() as conn:
            sql = (
                f'''
                INSERT INTO forecast_entity_shipment (
                CE_CODE,
                LAST_DATE,
                FIRST_NEXT_DATE,
                DAYS_FOR_FILLING
                ) VALUES (
                {ce_code},
                '{last_shipment}',
                '{next_shipment}',
                ARRAY {days_for_filling}
                 )'''
                )
            conn.execute(sql)

    def get_costs(self):
        sql = f'''
            select *
            from cost
            '''

        df = pd.read_sql(sql, self.connectable)

        return df

    def add_plans(self):
        # положить планы в бд
        pass


engine = create_engine(get_db_connection_str())

db = DiplomDB(engine)
