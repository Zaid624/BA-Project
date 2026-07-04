# BA Project - Superstore Data Analysis

This project fetches and displays data from the "Superstore Data" PostgreSQL table.

## Setup

### 1. Virtual Environment

The project uses a Python virtual environment (`.venv`) to manage dependencies.

#### Windows - PowerShell
```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Deactivate
deactivate
```

#### Windows - Command Prompt
```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Deactivate
deactivate
```

#### Quick Start (Windows)
Simply double-click `activate.bat` to activate the virtual environment, or `run.bat` to run the main script.

### 2. Install Dependencies

If you need to reinstall dependencies:
```bash
# With virtual environment activated
pip install -r requirements.txt
```

### 3. Environment Variables

Ensure you have a `.env` file in the project root with:
```
DATABASE_URL=your_database_connection_string
```

## Verify Setup

Check if everything is configured correctly:
```cmd
.venv\Scripts\python check_env.py
```

## Running the Project

### Option 1: Using the batch script (Easiest)
```cmd
run.bat
```

### Option 2: Manual execution
```cmd
# Activate virtual environment
.venv\Scripts\activate.bat

# Run the script
python main.py
```

### Option 3: Direct execution with venv Python
```cmd
.venv\Scripts\python main.py
```

## Output

The script will:
- Connect to your PostgreSQL/Supabase database
- Fetch all records from the "Superstore Data" table
- Display them in a formatted table
- Show the total count (9994 rows)

### Sample Output:
```
Connecting to database...
Connected successfully!

Ship Mode       | Segment         | Country         | City            | State           | ...
==================================================================================
Second Class    | Consumer        | United States   | Henderson       | Kentucky        | ...
Second Class    | Consumer        | United States   | Henderson       | Kentucky        | ...
...

Total rows: 9994

Database connection closed.
```

## Dependencies

- `psycopg2-binary` - PostgreSQL database adapter
- `python-dotenv` - Environment variable management

## Database Schema

Table: `public."Superstore Data"`

Columns:
- Ship Mode (text)
- Segment (text)
- Country (text)
- City (text)
- State (text)
- Postal Code (bigint)
- Region (text)
- Category (text)
- Sub-Category (text)
- Sales (double precision)
- Quantity (bigint)
- Discount (double precision)
- Profit (double precision)

## Troubleshooting

### Database Connection Issues

If you see "could not translate host name" error:
1. Check your internet connection
2. Verify the DATABASE_URL in `.env` is correct
3. Ensure your Supabase database is active (may need to wake it up from the dashboard)
4. Confirm the database server is accessible
