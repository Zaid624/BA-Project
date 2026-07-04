import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in .env file")
    exit(1)

try:
    # Connect to the database
    print("Connecting to database...")
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    print("Connected successfully!\n")

    # Query to fetch all data from Superstore Data table
    query = 'SELECT * FROM public."Superstore Data"'
    cursor.execute(query)

    # Fetch all rows
    rows = cursor.fetchall()

    # Get column names
    column_names = [desc[0] for desc in cursor.description]

    # Print column headers
    header = " | ".join(f"{col:15}" for col in column_names)
    print(header)
    print("=" * len(header))

    # Print each row
    for i, row in enumerate(rows, 1):
        formatted_row = " | ".join(
            f"{str(value) if value is not None else 'NULL':15}" for value in row
        )
        print(formatted_row)

    print("\n" + "=" * len(header))
    print(f"Total rows: {len(rows)}")

except psycopg2.OperationalError as e:
    print(f"Database connection error: {e}")
    print("\nPlease check:")
    print("1. Your internet connection")
    print("2. The DATABASE_URL in your .env file")
    print("3. Database server is accessible")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close cursor and connection
    try:
        if "cursor" in locals():
            cursor.close()
        if "connection" in locals():
            connection.close()
            print("\nDatabase connection closed.")
    except:
        pass
