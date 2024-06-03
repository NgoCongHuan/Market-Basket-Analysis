import pandas as pd
import numpy as np
import pyodbc
import requests
import sys
from pandas import json_normalize
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import time
import random

# Create List of Frequent itemsets 
def generate_frequent_itemsets(df_products):

    list_json_frequent_itemsets = []

    for _ in range(0, 3):

        n_sample = np.random.randint(2,4)

        df_frequent_itemsets = df_products.sample(n=n_sample, replace=False)

        index_to_drop = list(df_frequent_itemsets.index)

        df_products = df_products.drop(index_to_drop)

        json_frequent_itemsets = df_frequent_itemsets.to_dict('records')

        list_json_frequent_itemsets.append(json_frequent_itemsets)
    
    return list_json_frequent_itemsets

# Create Products of each Transactions
def generate_random_products(df_products, list_json_frequent_itemsets):

    random_products = []

    # Create random quantity sample product
    n_sample = np.random.randint(1,6)

    # Random sample products
    df_products = df_products.sample(n=n_sample, replace=False)

    json_frequent_itemsets = random.choice(list_json_frequent_itemsets)

    df_json_frequent_itemsets = pd.DataFrame(json_frequent_itemsets)

    df_products = pd.concat([df_products, df_json_frequent_itemsets], ignore_index=True)

    df_products = df_products.drop_duplicates(subset='p_id')

    # Create list random products
    for i in range(df_products.shape[0]):

        random_product = {}

        random_product['p_id'] = df_products['p_id'].iloc[i]
        random_product['p_price'] = df_products['p_price'].iloc[i]
        random_product['p_quantity'] = np.random.randint(1,3)

        random_products.append(random_product)

    return random_products

# Create Time of Transaction
def generate_random_time(day):

    # Get the current date
    now = datetime.now() + timedelta(days=day)
    start = datetime(now.year, now.month, now.day, 7)

    # Parameters for random time
    random_hours = np.random.randint(0, 15)
    random_minutes = np.random.randint(0, 61)
    random_seconds = np.random.randint(0, 61)
    
    # Create random time with start and parameter
    random_time = start + timedelta(hours=random_hours) + timedelta(minutes=random_minutes) + timedelta(seconds=random_seconds)
    
    # Format random time
    random_time = random_time.strftime('%Y-%m-%d %H:%M:%S')

    return random_time

# Create Transaction
def generate_transactions(df_products, list_json_frequent_itemsets, total, day):

    transaction_detail = []

    transactions = []

    for t_id in range(1, total+1):

        t_date = generate_random_time(day)

        t_total = 0

        random_products = generate_random_products(df_products, list_json_frequent_itemsets)

        for transaction in random_products:

            transaction['t_id'] = t_date.split(' ')[0].replace('-', '') + str(t_id) 

            transaction_detail.append(transaction)

            t_total += (transaction['p_price'] * transaction['p_quantity'])

        t_id = t_date.split(' ')[0].replace('-', '') + str(t_id) 

        transactions.append({'t_id': t_id, 't_date': t_date, 't_total': t_total})
    
    df_transactions = json_normalize(transactions)
    df_transaction_detail = json_normalize(transaction_detail)
        
    return df_transactions, df_transaction_detail

if __name__ == '__main__':

    # Parameter for connection
    server = 'DESKTOP-AL8SAM5'
    database = 'EmartShopping'
    username = 'sa'
    password = 'huan181102'

    # Create SQLAlchemy engine
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

    # Connection SQL Server
    try:
        
        conn = pyodbc.connect('DRIVER={SQL Server};' + f'SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()
        print('Connection SQL Server Successfully')

    except:

        print('Connection SQL Server Unsuccessfully')

    # Read data and convert to Dataframe
    df_products = pd.read_sql_query('SELECT p_id, p_price FROM Products', engine)
    
    # Create List Frequent itemsets
    list_json_frequent_itemsets = generate_frequent_itemsets(df_products)

    # Create Transaction in 30 Days
    for day in range(0,29):

        total = np.random.randint(400,1500) # Total is Number of Day

        # Generate Transactions
        df_transactions, df_transaction_detail = generate_transactions(df_products, list_json_frequent_itemsets, total, day)

        # Insert Transactions
        for index, row in df_transactions.iterrows():

            try:

                cursor.execute("INSERT INTO Transactions (t_id, t_date, t_total) VALUES(?,?,?)", row.t_id, row.t_date, row.t_total)
                sys.stdout.write(row.t_date.split(' ')[0])
                sys.stdout.write(f' Data at Index {index} has been inserted to the Transactions table\r')
                time.sleep(0.01)

            except requests.exceptions.RequestException as e:

                sys.stdout.write(f'Error at Index {index} of Transactions: {e}')
        
        sys.stdout.write('\n')

        # Insert Transaction Detail
        for index, row in df_transaction_detail.iterrows():

            try:

                cursor.execute("INSERT INTO Transaction_Detail (t_id, p_id, p_price, p_quantity) VALUES(?,?,?,?)", row.t_id, row.p_id, row.p_price, row.p_quantity)
                sys.stdout.write(f'Data at Index {index} has been inserted to the Transaction Detail table\r')
                time.sleep(0.01)

            except requests.exceptions.RequestException as e:

                sys.stdout.write(f'Error at Index {index} of Transactions: {e}')
        
        sys.stdout.write('\n')
    
    sys.stdout.write('All Transactions have been Inserted to Transactions table')
    
    # Commit and Close
    cursor.commit()
    cursor.close()
