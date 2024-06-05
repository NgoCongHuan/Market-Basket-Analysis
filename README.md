# Market Basket Analysis Emart Shopping

This project performs Market Basket Analysis in [Emart Viet Nam](https://emartmall.com.vn/) using transactional data. It includes data crawling, transaction generation, and analysis using association rule mining.

## Table of Contents
- [Project Structure](#Project-Structure)
- [Dashboard Preview](#Dashboard-Preview)
- [Step by Step to Set Up and Run the Project](#Step-by-Step-to-Set-Up-and-Run-the-Project)
- [Additional Notes](#Additional-Notes)
- [Contact](#Contact)

## Project Structure
```
Market-Basket-Analysis/
├── assets/
│   └── EmartShoppingDashboard.png
├── database/
│   └── EmartShopping.sql
├── insights/
│   └── EmartShopping.ppix
├── scripts/
│   ├── Crawl-Data.py
│   ├── Generate-Transactions.py
│   └── Market-Basket-Analysis.py
├── requirement.txt
└── README.md
```
- `database/`: Contains the SQL file to create the database.
- `insights/`: Contains the Power BI insights file.
- `scripts/`: Contains the scripts for crawling data, generating transactions, and performing market basket analysis.

## Dashboard Preview

![EmartShopping-Dashboard](/assets/EmartShoppingDashboard.png)

## Step by Step to Set Up and Run the Project

### 1. Install Requirements

First, ensure you have Python installed. Then, install the required packages:

```bash
pip install -r requirement.txt
```

### 2. Create Database
Create the database using the SQL file provided in the database folder:

- Open your SQL database client.
- Execute the SQL script EmartShopping.sql located in the database folder.

### 3. Change Parameters to Connect to SQL 
Update the database connection parameters in the scripts as needed (e.g., in Crawl-Data.py, Generate-Transactions.py, and Market-Basket-Analysis.py).

### 4. Run Scripts in Sequence
Run the scripts in the following order:
- Crawl Data: This script crawls the data and stores it in the SQL database.
```bash
python scripts/Crawl-Data.py
```
- Generate Transactions: This script generates transaction data from the crawled data.
```bash
python scripts/Generate-Transactions.py
```
- Market Basket Analysis: This script performs market basket analysis on trading data using the [Apriori algorithm](https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/)
```bash
python scripts/Market-Basket-Analysis.py
```

### 5. Connect Power BI to SQL Server Management Studio
Open File [EmartShoppingDashboard.ppix](/insights/EmartShoppingDashboard.ppix) and Get Data from SQL Server:
- Server: Your server's name in SQL Server
- Database: EmartShopping
- Data Connectivity mode: DirectQuery

## Additional Notes
This project crawl data in Emart Shopping website:  
- The Company: THISO RETAIL
- Link: [EmartShopping](https://emartmall.com.vn/)

## Contact
If you have any questions, please contact via email at ngohuan18112002@gmail.com
