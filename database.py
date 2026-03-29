import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables (optional, defaults provided)
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Chotu2006#")  # Change as required
DB_NAME = os.getenv("DB_NAME", "water_ai_db")

def get_connection():
    """Returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"\n[!] Error connecting to MySQL: {e}")
        return None

def initialize_database():
    """Initializes the database using schema.sql."""
    # Connecting without a specific database to create it if it doesn't exist
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Read schema.sql
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            if not os.path.exists(schema_path):
                print(f"[!] {schema_path} not found.")
                return False

            with open(schema_path, 'r') as f:
                sql_script = f.read()

            # Execute the script (Handles multiple statements)
            # This is a basic parser. For complex scripts, a proper parser might be needed.
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            print(f"[-] Error executing statement: {e}")
            
            connection.commit()
            print("[+] Database initialized successfully.")
            return True
            
    except Error as e:
        print(f"\n[!] Error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
