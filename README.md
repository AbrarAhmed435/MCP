# 💰 X-Tracker — MCP Expense Tracker

X-Tracker is a lightweight **MCP (Model Context Protocol) server** that lets you track and analyze expenses using natural language via tools integrated with Claude Desktop.

It demonstrates how to build **stateful AI tools** backed by a database and exposed through MCP.

---

## 🚀 Features

* ➕ Add expenses (date, category, amount)
* 📊 Get total expenses
* 🧾 Category-wise expense tracking
* 📅 Date range filtering
* 📈 Category breakdown within date range
* ⚡ Built using FastMCP + SQLite + uv

---

## 📁 Project Structure

```
ex_tracker/
├── main.py              # MCP server
├── expenses.db          # SQLite database (auto-created)
├── pyproject.toml       # Dependencies
├── uv.lock              # Lock file
├── commands.txt         # Useful commands
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```
git clone <your-repo-url>
cd ex_tracker
```

---

### 2️⃣ Create virtual environment using uv

```
uv venv
```

(Optional activate)

```
source .venv/bin/activate
```

---

### 3️⃣ Install dependencies

```
uv sync
```

---

## 🧪 Test the MCP Server (Local UI)

Run the development UI to test tools:

```
uv run mcp dev main.py
```

👉 This will open a UI where you can:

* View all tools
* Execute them manually
* Debug responses

---

## 🔌 Add to Claude Desktop

### 1️⃣ Open config file

```
nano ~/.config/Claude/claude_desktop_config.json
```

---

### 2️⃣ Add this inside "mcpServers"

```
uv run mcp install main.py
```
OR
```
"ex-tracker": {
  "command": "/home/<your-username>/.local/bin/uv",
  "args": [
    "run",
    "--frozen",
    "--with",
    "mcp[cli]",
    "mcp",
    "run",
    "/absolute/path/to/ex_tracker/main.py"
  ]
}
```

⚠️ Replace:

* `<your-username>`
* `/absolute/path/to/ex_tracker/main.py`

---

### 3️⃣ Restart Claude Desktop

After restarting:

* Go to **Connected MCP Servers**
* You should see: ✅ `ex-tracker`

---

## 🧠 Example Prompts (in Claude)

* “Add ₹500 food expense today”
* “What is my total expense?”
* “How much did I spend on travel?”
* “Show category breakdown for January”
* “Expenses between 2026-01-01 and 2026-01-31”

---

## 🛠️ Tools Implemented

* `add_expense`
* `get_total_expense`
* `get_expenses_by_category`
* `get_expenses_by_date_range`
* `get_category_breakdown_by_date_range`

---

## 🧠 Tech Stack

* Python
* SQLite
* FastMCP
* uv
* Claude Desktop (MCP client)

---

## ⚠️ Notes

* Dates must be in `YYYY-MM-DD` format
* Database is auto-created on first run
* Uses parameterized SQL queries (safe from injection)
* Uses absolute paths for MCP compatibility

---

## 🚀 Future Improvements

* Monthly summaries
* Top spending category
* Budget tracking
* Export to CSV
* Dashboard UI

---

## ⭐ If you found this useful

Give it a ⭐ and share your feedback!

---

## 📬 Connect

Built while exploring **Agentic AI + MCP systems**

Let’s connect 🚀
