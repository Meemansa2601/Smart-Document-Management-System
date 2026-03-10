import sqlite3
import pandas as pd
from datetime import datetime

# The name of your local database file
DB_NAME = 'smart_vault.db'

def init_db():
    """
    Initializes the database. 
    Creates the 'documents' table if it doesn't already exist.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Table structure to support Timeline, Expenses, and Tax features
    c.execute('''CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    category TEXT,
                    summary TEXT,
                    amount REAL,
                    alert_date TEXT,
                    upload_date TEXT
                 )''')
    conn.commit()
    conn.close()

def save_document_data(filename, category, summary, amount, alert_date):
    """
    Saves the AI-extracted insights into the database.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Get current timestamp for the upload date
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Insert data into the table
    c.execute('''INSERT INTO documents (filename, category, summary, amount, alert_date, upload_date)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (filename, category, summary, amount, alert_date, now))
    
    conn.commit()
    conn.close()

def get_all_documents():
    """
    Retrieves all stored documents as a Pandas DataFrame.
    This is used for the 'Life Timeline View' and 'Tax Folder'.
    """
    conn = sqlite3.connect(DB_NAME)
    # Using Pandas makes it very easy to display in Streamlit
    df = pd.read_sql_query("SELECT * FROM documents ORDER BY upload_date DESC", conn)
    conn.close()
    return df

def get_tax_documents():
    """
    Special filter for the 'One-Tap Tax Folder' feature.
    """
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM documents WHERE category IN ('Bills', 'Receipts', 'Banking', 'Legal')"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df