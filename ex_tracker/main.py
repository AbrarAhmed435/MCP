import sqlite3
from mcp.server.fastmcp import FastMCP
import os

mcp=FastMCP("ex-tracker")

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.path.join(BASE_DIR,"expenses.db")


conn=sqlite3.connect(DB_PATH,check_same_thread=False)

cursor=conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               date TEXT NOT NULL,
               category TEXT NOT NULL,
               price REAL NOT NULL               
)
""")
conn.commit()




@mcp.tool()
def add_expense(date: str, category:str,price:float)->str:
    """
    Add a new expense entry . 
    Args:
        data:Date of expense (YYYY-MM-DD)
        category: Expense category (eg. food travel etc)
        price: amount spend in INR

    Returns:
        Confirmation message
    """
    if price<=0:
        raise ValueError("Price must be positive")
    cursor.execute(
        "INSERT INTO expenses (date, category, price) VALUES (?,?,?)",
        (date,category,price)
    )
    conn.commit()
    return "Expense added successfully"


@mcp.tool()
def mcp_total_expense()->float:
    """
    Calculate total expense so far.
    Returns
        Total sum of all expense
    """
    cursor.execute("SELECT SUM(price) FROM expenses")
    result=cursor.fetchone()[0]

    return result if result else 0.0

if __name__ == "__main__":
    mcp.run()