import json

import os

import pandas as pd

import numpy as np

from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .telegram import Telegram

class JSONHandler:
    def __init__(self):
        self.HOST = os.getenv('db_host')
        self.PORT = os.getenv('db_port')
        self.USER = os.getenv('db_user')
        self.PASSWORD = os.getenv('db_password')

    def get_connection_string(self) -> str:
        return (
            f'mysql+mysqlconnector://{self.USER}:'
            f'{self.PASSWORD}@{self.HOST}:{self.PORT}'
        )

    def get_columns(self) -> dict:
        return self._load_json('./json/columns.json')

    def _load_json(self, path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)

class FILEHandler:
    def __init__(self):
        self.download_path = self._get_download_path()
        self.file = None

    def _get_download_path(self) -> str:
        home = Path.home()
        return os.path.join(home, 'Downloads')

    def read(self, filename: str = 'pivot.csv') -> pd.DataFrame:
        try:
            if filename == 'pivot.csv':
                self.file = filename
                return pd.read_csv(
                    os.path.join(self.download_path, filename),
                    delimiter=',', encoding='utf-8'
                )
            else:
                for file in os.listdir(self.download_path):
                    self.file = file
                    if filename in file and filename == 'sales':
                        return pd.read_excel(
                                os.path.join(self.download_path, file),
                                engine='openpyxl'
                            )
                    elif filename in file and filename == 'Servico':
                        return pd.read_html(
                            os.path.join(self.download_path, file), flavor='lxml'
                        )
        except FileNotFoundError:
            Telegram(f'\ndblinx | 🗃️ {filename} not found')
            return pd.DataFrame()

    def delete_file(self):
        try:
            os.remove(os.path.join(self.download_path, self.file))
        except FileNotFoundError:
            Telegram(f'\ndblinx | 🗃️ {self.file} not found to delete')

class EmployeesUpsert(JSONHandler, FILEHandler):
    def __init__(self):
        print('Upsert: employees')
        JSONHandler.__init__(self)
        FILEHandler.__init__(self)
        self.df = self.read()
        if not self.df.empty:
            self.engine = create_engine(self.get_connection_string())
            self.session = sessionmaker(bind=self.engine)()
            self.columns = self.get_columns()['employees']
            self._process_data()
            self._upsert_data()

    def _process_data(self) -> pd.DataFrame:
        try:
            self.df.rename(columns=self.columns, inplace=True)
            self.df.replace({'(blank)': None, pd.NaT: None, np.nan: None}, inplace=True)
            
            self.df['admission_date'] = self.df['admission_date'].str.split(' ').str[0]
            self.df['admission_date'] = pd.to_datetime(self.df['admission_date'], format=f'%m/%d/%Y')

            self.df['termination_date'] = self.df['termination_date'].str.split(' ').str[0]
            self.df['termination_date'] = pd.to_datetime(self.df['termination_date'], format=f'%d/%m/%Y')

            self.df['id'] = pd.to_numeric(self.df['id'].str.split(',').str[0]).astype(int)
            self.df['store_id'] = pd.to_numeric(self.df['store_id'].str.split(',').str[0]).astype(int)
            self.df['phone_number'] = pd.to_numeric(self.df['phone_number']).astype(float).round(0)
            self.df['professional_whatsapp'] = pd.to_numeric(self.df['professional_whatsapp']).astype(float).round(0)

            numeric_cols = ['professional_whatsapp', 'phone_number']
            for col in numeric_cols:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

            self.df['active'] = self.df['active'].map({'Sim': 1, 'Não': 0})
            print(f'Process data: with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Porcess data with error for employees')
        finally:
            self.delete_file()

    def _upsert_data(self):
        try:
            self.df.to_sql(name='temp_employees', schema='dball', con=self.engine, if_exists='replace', index=False)

            query = f"""
                INSERT INTO dblinx.employees ({', '.join(self.df.columns)})
                SELECT * FROM dball.temp_employees
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in self.df.columns])}
            """

            with self.session.connection() as connection:
                connection.execute(text(query))
                connection.execute(text('DROP TABLE dball.temp_employees'))
            print(f'upsert with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Upsert data with error for employees')

class SalesUpsert(JSONHandler, FILEHandler):
    def __init__(self):
        print(f'Upsert: sales')
        JSONHandler.__init__(self)
        FILEHandler.__init__(self)
        self.df_sales = self.read()
        if not self.df_sales.empty:
            self.engine = create_engine(self.get_connection_string())
            self.session = sessionmaker(bind=self.engine)()
            self.columns = self.get_columns()['sales']
            self._process_data()
            self._upsert_data()

    def _process_data(self):
        try:
            self.df_sales.replace({'(Blank)': '', pd.NaT: None, np.nan: None}, inplace=True)

            self.df_sales.rename(columns=self.columns, inplace=True)
            self.df_sales.reset_index(drop=True, inplace=True)

            self.df_sales['id'] = self.df_sales.apply(lambda row: int(f"{row['store_id']}{row['document']}{row['product_id']}"), axis=1)
            self.df_sales['employee_id'] = self.df_sales['employee_name'].str.split(' - ').str[0].astype(int)

            self.df_sales['registration_date'] = pd.to_datetime(self.df_sales['registration_date'], format='%d/%m/%Y')
            self.df_sales['item_value'] = pd.to_numeric(self.df_sales['item_value'].str.replace('.', '').str.replace(',', '.'), errors='coerce').round(2)
            self.df_sales['item_discount'] = pd.to_numeric(self.df_sales['item_discount'].str.replace('.', '').str.replace(',', '.'), errors='coerce').round(2)
            self.df_sales['item_quantity'] = pd.to_numeric(self.df_sales['item_quantity'], errors='coerce')

            self.df_customers = self.df_sales[['customer_id', 'customer_name', 'customer_cpf']].drop_duplicates()
            self.df_customers.rename(columns={
                'customer_id': 'id',
                'customer_name': 'name',
                'customer_cpf': 'cpf'
            }, inplace=True)

            self.df_sales.drop(columns=[
                'customer_name',
                'customer_cpf',
            ], inplace=True)

            self.df_customers.reset_index(drop=True, inplace=True)
            print(f'process with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Porcess data with error for employees')
            self.delete_file()
        finally:
            self.delete_file()

    def _upsert_data(self):
        try:
            self.df_sales.to_sql(name='temp_sales', schema='dball', con=self.session.connection(), if_exists='replace', index=False)
            self.df_customers.to_sql(name='temp_customers', schema='dball', con=self.session.connection(), if_exists='replace', index=False)

            queries = [
                f"""
                INSERT INTO dblinx.customers ({', '.join(self.df_customers.columns)})
                SELECT * FROM dball.temp_customers
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in self.df_customers.columns])}
                """,
                f"""
                INSERT INTO dblinx.sales ({', '.join(self.df_sales.columns)})
                SELECT * FROM dball.temp_sales
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in self.df_sales.columns])}
                """
            ]

            with self.session.connection() as connection:
                for query in queries:
                    connection.execute(text(query))
                connection.execute(text('DROP TABLE IF EXISTS dball.temp_sales, dball.temp_customers'))
            print(f'upsert with success')
        except Exception:
            Telegram(f'\ndblinx | ⛔ Upsert data with error for sales and customers')

class MobilePlansUpsert(JSONHandler, FILEHandler):
    def __init__(self):
        print(f'Upsert: mobile plans')
        JSONHandler.__init__(self)
        FILEHandler.__init__(self)
        self.df = self.read(filename='sales')
        if not self.df.empty:
            self.engine = create_engine(self.get_connection_string())
            self.session = sessionmaker(bind=self.engine)()
            self.columns = self.get_columns()['mobile_plans']
            self._process_data()
            self._upsert_data()

    def _process_data(self):
        try:
            self.df.rename(columns=self.columns, inplace=True)
            self.df.replace({'(Blank)': '', pd.NaT: None, np.nan: None}, inplace=True)

            columns_for_drop = list()
            for col in self.df.columns:
                if col not in self.columns.values():
                    columns_for_drop.append(str(col))

            self.df.drop(columns=columns_for_drop, inplace=True)
            self.df.reset_index(drop=True, inplace=True)

            self.df['registration_date'] = pd.to_datetime(self.df['registration_date'], format=f'%d/%m/%Y')
            print(f'process with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Porcess data with error for mobile plans')
        finally:
            self.delete_file()

    def _upsert_data(self):
        try:
            self.df.to_sql(name='temp_mobile_plans', schema='dball', con=self.session.connection(), if_exists='replace', index=False)

            query = f"""
                INSERT INTO dblinx.mobile_plans ({', '.join(self.df.columns)})
                SELECT * FROM dball.temp_mobile_plans
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in self.df.columns])}
                """

            with self.session.connection() as connection:
                connection.execute(text(query))
                connection.execute(text('DROP TABLE IF EXISTS dball.temp_mobile_plans'))
            print(f'upsert with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Upsert data with error for mobile plans')
        
class InsuranceUpsert(JSONHandler, FILEHandler):
    def __init__(self):
        print(f'Upsert: insurance')
        JSONHandler.__init__(self)
        FILEHandler.__init__(self)
        self.df = self.read(filename='Servico')[0]
        if not self.df.empty:
            self.engine = create_engine(self.get_connection_string())
            self.session = sessionmaker(bind=self.engine)()
            self.columns = self.get_columns()['insurance']
            self._process_data()
            self._upsert_data()

    def _process_data(self):
        try:
            self.df.rename(columns=self.columns, inplace=True)
            self.df.replace({'(Blank)': '', pd.NaT: None, np.nan: None}, inplace=True)

            columns_for_drop = list()
            for col in self.df.columns:
                if col not in self.columns.values():
                    columns_for_drop.append(str(col))

            self.df['store_id'] = self.df['store_id'].str.split(' ').str[0].astype(int)
            self.df['registration_date'] = pd.to_datetime(self.df['registration_date'], format=f'%d/%m/%Y')
            self.df['issue_date'] = pd.to_datetime(self.df['issue_date'], format=f'%d/%m/%Y')
            self.df['adhesion_date'] = pd.to_datetime(self.df['adhesion_date'], format=f'%d/%m/%Y')
            self.df['validity_start_date'] = pd.to_datetime(self.df['validity_start_date'], format=f'%d/%m/%Y')
            self.df['validity_end_date'] = pd.to_datetime(self.df['validity_end_date'], format=f'%d/%m/%Y')
            self.df['nf_date'] = pd.to_datetime(self.df['nf_date'], format=f'%d/%m/%Y')

            self.df['is_canceled'] = self.df['is_canceled'].map({'Sim': 1, 'Não': 0})

            self.df.drop(columns=columns_for_drop, inplace=True)
            self.df.reset_index(drop=True, inplace=True)

            self.df['registration_date'] = pd.to_datetime(self.df['registration_date'], format=f'%d/%m/%Y')
            print(f'process with success')
        except Exception:
            Telegram('Process data with error for insurance')
        finally:
            self.delete_file()

    def _upsert_data(self):
        try:
            self.df.to_sql(name='temp_insurance_sales', schema='dball', con=self.session.connection(), if_exists='replace', index=False)

            query = f"""
                INSERT INTO dblinx.insurance_sales ({', '.join(self.df.columns)})
                SELECT * FROM dball.temp_insurance_sales
                ON DUPLICATE KEY UPDATE
                    {', '.join([f'{col} = VALUES({col})' for col in self.df.columns])}
                """

            with self.session.connection() as connection:
                connection.execute(text(query))
                connection.execute(text('DROP TABLE IF EXISTS dball.temp_insurance_sales'))
            print(f'upsert with success')
        except Exception:
            Telegram('\ndblinx | ⛔ Upsert data with error')
