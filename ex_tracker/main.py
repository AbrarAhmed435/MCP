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

cursor.execute("PRAGMA table_info(expenses)")
columns = [col[1] for col in cursor.fetchall()]

if "subcategory" not in columns:
    cursor.execute("ALTER TABLE expenses ADD COLUMN subcategory TEXT")
    conn.commit()
conn.commit()




@mcp.tool()
def add_expense(date: str, category:str,subcategory:str,price:float)->str:
    """
    Add a new expense entry . 
    Args:
        data:Date of expense (YYYY-MM-DD)
        category: Expense category (eg. food travel etc)
        subcategory: 
        price: amount spend in INR

    Returns:
        Confirmation message
    """
    if price<=0:
        raise ValueError("Price must be positive")
    cursor.execute(
        "INSERT INTO expenses (date, category,subcategory, price) VALUES (?,?,?,?)",
        (date,category,subcategory,price)
    )
    conn.commit()
    return {
        "message":"Expense added Successfully"
    }


@mcp.tool()
def mcp_total_expense()->float:
    """
    Calculate total expense so far.
    Returns
        Total sum of all expense
    """
    cursor.execute("SELECT SUM(price) FROM expenses")
    result=cursor.fetchone()[0]

    return {
        "total_spending":result or 0.0
    }


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
        (f"%{category}%",)
    )
    result=cursor.fetchone()[0]
    return {
        "category":category,
        "total":result or 0.0
    }



@mcp.tool()
def get_expense_breakdown_by_category()->dict:
    """
    "overall_total"
        "top_category expense wise"
        "top_10 categories "
        "smallest_10 categories"
    """
    cursor.execute(
        """
        SELECT category,subcategory,SUM(price) as total FROM expenses GROUP BY LOWER (category), LOWER(subcategory)
        ORDER BY total DESC
        """
    )

    rows=cursor.fetchall()

    result={}
    overall_total=0

    for category,subcategory,total in rows:
        category=category.lower()
        subcategory=(subcategory or "unknown").lower()

        if category not in result:
            result[category]={"total":0}

        result[category][subcategory]=total
        result[category]["total"]+=total
    overall_total = sum(data["total"] for data in result.values())
    top_10=rows[:10]
    bottom_10 = rows[-10:][::-1]
    top_count=0
    top_category=""
    for category,data in result.items():
        # if category=="overall_total":
        #     continue
        if data["total"]>top_count:
            top_count=data["total"]
            top_category=category
    result["overall_total"]=overall_total
    result["top_category"]={
        "category":top_category,
        "total":top_count,
        "percentage_share":round(top_count/overall_total,2) if overall_total else 0
    }

    result["top_10"]=[
        {
            "category":c.lower(),
            "subcategory":(s or "unknown").lower(),
            "total":t
        }
        for c, s, t in top_10
    ]
    result["bottom_10"]=[
        {
            "category":c.lower(),
            "subcategory":(s or "unknown").lower(),
            "total":t
        }
        for c, s, t in bottom_10
    ]
    return {
        "overall_total":result["overall_total"],
        "top_category":result["top_category"],
        "top_10":result["top_10"],
        "bottom_10":result["bottom_10"]
    }




def get_breakdown(start_date: str, end_date: str) -> dict:
    """
    Get category-wise expense breakdown within a date range.
    """

    cursor.execute(
        """
        SELECT category, subcategory, SUM(price) as total
        FROM expenses
        WHERE date BETWEEN ? AND ?
        GROUP BY LOWER(category), LOWER(subcategory)
        ORDER BY total DESC
        """,
        (start_date, end_date)
    )

    rows = cursor.fetchall()

    result = {}

    # Build structure
    for category, subcategory, total in rows:
        category = category.lower()
        subcategory = (subcategory or "unknown").lower()

        if category not in result:
            result[category] = {"total": 0}

        result[category][subcategory] = total
        result[category]["total"] += total

    # Overall total
    overall_total = sum(data["total"] for data in result.values())

    # Top & bottom
    top_10 = rows[:10]
    bottom_10 = rows[-10:][::-1]

    # Top category
    top_category = ""
    top_count = 0

    for category, data in result.items():
        if data["total"] > top_count:
            top_count = data["total"]
            top_category = category

    return {
        "overall_total": overall_total,
        "top_category": {
            "category": top_category,
            "total": top_count,
            "percentage_share": round(top_count / overall_total, 2) if overall_total else 0
        },
        "top_10": [
            {
                "category": c.lower(),
                "subcategory": (s or "unknown").lower(),
                "total": t
            }
            for c, s, t in top_10
        ],
        "bottom_10": [
            {
                "category": c.lower(),
                "subcategory": (s or "unknown").lower(),
                "total": t
            }
            for c, s, t in bottom_10
        ]
    }

@mcp.tool()
def get_category_breakdown_by_date_range(months_back: int):
    """
    Get category-wise expense breakdown for a past month.
    """
    from datetime import date, timedelta

    def subtract_months(d, months):
        year = d.year
        month = d.month - months

        while month <= 0:
            month += 12
            year -= 1

        return date(year, month, 1)

    today = date.today()

    # Get target month
    target = subtract_months(today, months_back)

    start_date = target

    # Get last day of month
    if target.month == 12:
        next_month = date(target.year + 1, 1, 1)
    else:
        next_month = date(target.year, target.month + 1, 1)

    end_date = next_month - timedelta(days=1)

    # Call your DB function
    result = get_breakdown(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    return {
        "month": target.strftime("%B %Y"),
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "data": result
    }

@mcp.tool
def get_last_n_days_breakdown(days: int):
    """
    Get expense breakdown in last n days
    """
    from datetime import date, timedelta

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    result = get_breakdown(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "data": result
    }

        

if __name__ == "__main__":
    mcp.run()

    