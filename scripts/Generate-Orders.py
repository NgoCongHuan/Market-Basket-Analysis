import pandas as pd
import numpy as np
import pyodbc
import requests
import sys
from pandas import json_normalize
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import time

def generate_random_products(df_products):

    random_products = []

    # Create random quantity sample product
    n_sample = np.random.randint(1,11)

    # Random sample products
    df_products = df_products.sample(n=n_sample, replace=False)

    # Create list random products
    for i in range(df_products.shape[0]):

        random_product = {}

        random_product['p_id'] = df_products['p_id'].iloc[i]
        random_product['p_price'] = df_products['p_price'].iloc[i]
        random_product['p_quantity'] = np.random.randint(1,6)

        random_products.append(random_product)

    return random_products

def generate_random_time():

    # Get the current date
    now = datetime.now()
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

def generate_orders(total):

    orders = []

    for o_id in range(1, total+1):

        o_date = generate_random_time()

        random_products = generate_random_products(df_products)

        for order in random_products:

            order['o_id'] = o_date.split(' ')[0].replace('-', '') + str(o_id) 
            order['o_date'] = o_date

            orders.append(order)
    
    df_orders = json_normalize(orders)
        
    return df_orders

if __name__ == '__main__':

    # Parameter for connection
    server = 'DESKTOP-AL8SAM5'
    database = 'EmartShopping'
    username = 'sa'
    password = 'huan181102'

    # Create SQLAlchemy engine
    engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

    # Read data and convert to Dataframe
    df = pd.read_sql_query('SELECT PC.p_id, p_price, cg_id FROM Products P right outer join Product_Categories PC on P.p_id = PC.p_id', engine)

    df_products = pd.DataFrame()

    for cg_id in df['cg_id'].unique():

        df_temp = df[df['cg_id'] == cg_id].sample(2)

        df_products = pd.concat([df_products, df_temp], ignore_index=True)
    
    # Generate Orders
    df_orders = generate_orders(738)

    # Connection SQL Server
    try:
        
        conn = pyodbc.connect('DRIVER={SQL Server};' + f'SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()
        print('Connection SQL Server Successfully')

    except:

        print('Connection SQL Server Unsuccessfully')

    # Insert Orders
    for index, row in df_orders.iterrows():

        try:

            cursor.execute("INSERT INTO Orders (o_date, o_id, p_id, p_price, p_quantity) VALUES(?,?,?,?,?)", row.o_date, row.o_id, row.p_id, row.p_price, row.p_quantity)
            sys.stdout.write(f'Data at Index {index} has been inserted to the Orders table\r')
            time.sleep(0.03)

        except requests.exceptions.RequestException as e:

            sys.stdout.write(f'Error at Index {index} of Orders: {e}')
    
    sys.stdout.write('\n')
    sys.stdout.write('All Orders have been Inserted to Orders table')
    
    cursor.commit()
    cursor.close()
