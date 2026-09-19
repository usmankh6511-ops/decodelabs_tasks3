"""
Project 3: The Data Warehouse — Azure version
Bonus - connect to Azure Database for MySQL Flexible Server from Python.

Install dependency first:
    pip install pymysql

Edit the CONFIG section below with your own values, then run:
    python connect_db.py
"""

import pymysql
import ssl

# ======================= CONFIG =======================
DB_HOST = "interns-mysql-server.mysql.database.azure.com"
DB_PORT = 3306
DB_USER = "dbadmin"          # do NOT use 'admin' — Azure MySQL reserves it
DB_PASSWORD = "your-db-password"
DB_NAME = "internsdb"
# ========================================================


def run_queries():
    # Azure Database for MySQL requires SSL by default
    ssl_ctx = ssl.create_default_context()

    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        ssl={"ssl": ssl_ctx},
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Interns;")
            rows = cursor.fetchall()
            print(f"{'InternID':<10}{'FirstName':<12}{'LastName':<12}{'Email':<30}{'Role':<15}")
            print("-" * 79)
            for row in rows:
                print(f"{row['InternID']:<10}{row['FirstName']:<12}{row['LastName']:<12}"
                      f"{row['Email']:<30}{row['Role']:<15}")
    finally:
        conn.close()


if __name__ == "__main__":
    run_queries()
