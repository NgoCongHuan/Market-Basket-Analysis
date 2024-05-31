import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import json_normalize
import pyodbc
from sqlalchemy import create_engine

def crawl_products(cg_link, cg_id):

    product_json = []
    page = 1
    
    while True:
        
        try:
           
            url = f'{cg_link}&page={page}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            responses = requests.get(headers=headers, url=url, timeout=100)
            responses.raise_for_status()

        except requests.exceptions.RequestException as e:
            
            continue

        soup = BeautifulSoup(responses.content, 'html.parser')

        products_block = soup.find_all('div', class_='product-block desktop-pdt')

        if len(products_block) > 0:

            for product in products_block:

                data = {}
                
                p_image = product.find('img', class_='img-responsive lazy-load').attrs['src']
                p_name = product.find('div', class_='name').text
                p_price = int(product.find('span', class_='price-new').text.replace('₫','').replace('.',''))
                p_link = product.find('div', class_='name').find('a').attrs['href']
                p_id = p_link.split('&')[-1].replace('product_id=', '')
                cg_id = cg_id

                data['p_image'] = p_image
                data['p_id'] = p_id.strip()
                data['p_name'] = p_name.strip()
                data['p_price'] = p_price
                data['cg_id'] = cg_id
                data['p_link'] = p_link

                product_json.append(data)
            
            sys.stdout.write(f'Category ID: {cg_id} | Page: {page} | Total Products: {len(product_json)}\r')
            sys.stdout.flush()
            
        else:
            
            print(f'{len(product_json)} Products of Category {cg_id} have been added successfully')
            break

        page += 1
    
    return product_json

def crawl_categories():

    try:
        
        responses = requests.get('https://sala.emartmall.com.vn/index.php?route=common/home', timeout=100)
        responses.raise_for_status()

    except requests.exceptions.RequestException as e:
        
        print(f'Error fetching in Homepage: {e}')
    
    soup = BeautifulSoup(responses.content, 'html.parser')
    
    categories = soup.find_all('li', class_='parent dropdown')

    categories_json = []

    products_json = []
    
    for category in categories:

        data = {}
        
        cg_name = category.find('span', class_='menu-title').text
        cg_link = category.find('a').attrs['href']
        cg_id = cg_link.split('&')[-1].replace('path=', '')
        
        data['cg_id'] = cg_id
        data['cg_name'] = cg_name.strip()
        data['cg_link'] = cg_link

        categories_json.append(data)

        product_json = crawl_products(cg_link, cg_id)

        products_json += product_json

    return categories_json, products_json

if __name__ == '__main__':
    
    categories_json, products_json = crawl_categories()
    
    df_categories = json_normalize(categories_json)
    df_products = json_normalize(products_json)

    # Parameter for connection
    server = 'DESKTOP-AL8SAM5'
    database = 'EmartShopping'
    username = 'sa'
    password = 'huan181102'

    # Connection SQL Server
    try:
        conn = pyodbc.connect('DRIVER={SQL Server};' + f'SERVER={server};DATABASE={database};UID={username};PWD={password}')
        cursor = conn.cursor()
        print('Connection SQL Server Successfully')
    except:
        print('Connection SQL Server Unsuccessfully')

    # Insert Data to Categories table
    for index, row in df_categories.iterrows():
        cursor.execute("INSERT INTO Categories (cg_id, cg_name, cg_link) VALUES(?,?,?)", row.cg_id, row.cg_name, row.cg_link)
        sys.stdout.write(f'Data at Index {index} has been inserted to the Categories table\r')
        sys.stdout.flush()
    sys.stdout.write('\n')

    # Insert Data to Products table
    for index, row in df_products.drop(['cg_id', 'p_link'], axis=1).drop_duplicates().iterrows():
        cursor.execute("INSERT INTO Products (p_image, p_id, p_name, p_price) VALUES(?,?,?,?)", row.p_image, row.p_id, row.p_name, row.p_price)
        sys.stdout.write(f'Data at Index {index} has been inserted to the Products table\r')
        sys.stdout.flush()
    sys.stdout.write('\n')

    # Insert Data to Product_Links table
    for index, row in df_products.iterrows():
        cursor.execute("INSERT INTO Product_Links (p_id, p_link) VALUES(?,?)", row.p_id, row.p_link)
        sys.stdout.write(f'Data at Index {index} has been inserted to the Product_Links table\r')
        sys.stdout.flush()
    sys.stdout.write('\n')

    # Insert Data to Product_Categories table
    for index, row in df_products[['p_id', 'cg_id']].drop_duplicates().iterrows():
        cursor.execute("INSERT INTO Product_Categories (p_id, cg_id) VALUES(?,?)", row.p_id, row.cg_id)
        sys.stdout.write(f'Data at Index {index} has been inserted to the Product_Categories table\r')
        sys.stdout.flush()
    sys.stdout.write('\n')

    sys.stdout.write('All data have been inserted successfully')

    cursor.commit()
    cursor.close()