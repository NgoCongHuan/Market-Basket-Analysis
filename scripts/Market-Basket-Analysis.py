import pandas as pd
from sqlalchemy import create_engine
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import apriori
import sys
import time
import requests
import pyodbc

# Parameter for connection
server = 'DESKTOP-AL8SAM5'
database = 'EmartShopping'
username = 'sa'
password = 'huan181102'

# Create SQLAlchemy engine
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server')

# Read data and convert to Dataframe
df_orders = pd.read_sql_query('SELECT t_id, p_id FROM Transaction_Detail', engine)

grouped = df_orders.groupby('t_id')['p_id'].apply(list)

list_grouped = list(grouped)

te = TransactionEncoder()
te_ary = te.fit(list_grouped).transform(list_grouped)
df_new = pd.DataFrame(te_ary, columns=te.columns_)

frequent_itemsets = apriori(df_new, min_support = 0.001 ,use_colnames=True)

if frequent_itemsets.empty:
    print('Frequent is empty')
else:
    df_rules = association_rules(frequent_itemsets, metric="confidence")
    
df_rules['antecedents'] = df_rules['antecedents'].apply(lambda x: list(x))
df_rules['consequents'] = df_rules['consequents'].apply(lambda x: list(x))

# Connection SQL Server
try:
    
    conn = pyodbc.connect('DRIVER={SQL Server};' + f'SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = conn.cursor()
    print('Connection SQL Server Successfully')

except:

    print('Connection SQL Server Unsuccessfully')

# Insert Orders
for index, row in df_rules.iterrows():

    try:

        cursor.execute(
        "INSERT INTO Market_Basket_Analysis (antecedents, consequents, antecedent_support, consequent_support, support, confidence, lift) VALUES(?,?,?,?,?,?,?)",
        (
            str(row['antecedents']), 
            str(row['consequents']), 
            row['antecedent support'], 
            row['consequent support'], 
            row['support'], 
            row['confidence'], 
            row['lift']
        )
    )
        sys.stdout.write(f'Data at Index {index} has been inserted to the Market_Basket_Analysis table\r')
        time.sleep(0.03)

    except requests.exceptions.RequestException as e:

        sys.stdout.write(f'Error at Index {index} of Orders: {e}')

sys.stdout.write('\n')
sys.stdout.write('All Orders have been Inserted to Orders table')

cursor.commit()
cursor.close()

