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


@mcp.tool()
def get_expenses_by_category(category:str)->float:
    """
    Get total expense for a specific category.

    Args:
        category: Expense category (e.g., food, travel)

    Returns:
        Total expense for that category
    """
    cursor.execute(
        "SELECT SUM(price) FROM expenses WHERE LOWER(category)=LOWER(?)",
        (category,)
    )
    result=cursor.fetchone()[0]
    return result if result else 0.0


@mcp.tool()
def get_expense_breakdown_by_category()->dict:
    """
    Get total expenses grouped by category
    Returns
     Dictionary with category as key and total expense as value
    """
    cursor.execute(
        "SELECT category, SUM(price) FROM expenses GROUP BY LOWER (category)"
    )
    rows=cursor.fetchall()
    result={}

    for row in rows:
        result[row[0]]=row[1]
    
    return result


# @mcp.tool()
# def get_expenses_by_date_range(start_date:str,end_date:str)->float:
#     """
#     Get total expenses bw two dates,
#     Args:
#         start_date:Start date(YYYY-MM-DD)
#         end_date:End date(YYYY-MM-DD)
#     Returns:
#         Total expense in that range
#     """
#     cursor.execute(
#         """
#         SELECT SUM(price)
#         FROM expenses
#         WHERE date BETWEEN ? AND ?
#         """,
#         (start_date,end_date,)
#     )

#     result=cursor.fetchone()[0]
    
#     return result if result else 0.0


@mcp.tool()
def get_category_breakdown_by_date_range(start_date: str, end_date: str) -> dict:
    """
    Get category-wise expense breakdown within a date range.

    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        Dictionary with category as key and total expense as value
    """
    cursor.execute(
        """
        SELECT category, SUM(price)
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY LOWER(category)
        """,
        (start_date, end_date)
    )

    rows = cursor.fetchall()
    result={}
    for row in rows:
        result[row[0]]=row[1]

    total_expense=0
    for a,b in result.items():
        total_expense+=b

    return result,total_expense

if __name__ == "__main__":
    mcp.run()