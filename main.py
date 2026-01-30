from mcp.server.fastmcp import FastMCP
import sqlite3
import os

mcp = FastMCP("sqlite-mcp")

DEFAULT_DB_NAME = "Chinook_Sqlite.sqlite"


def get_db_path(user_path: str = None) -> str:
    """
    Determines which database file to use.
    Priority 1: The path the user provided in the prompt.
    Priority 2: The default file in the same directory as this script.
    """
    if user_path:
        return user_path

    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(current_dir, DEFAULT_DB_NAME)

    if not os.path.exists(default_path):
        raise FileNotFoundError(
            f"No path provided and default '{DEFAULT_DB_NAME}' not found in {current_dir}"
        )

    return default_path


@mcp.tool()
def list_tables(db_path: str = None) -> str:
    """
    Returns a list of all table names.
    Args:
        db_path: (Optional) Path to the .db file. If not provided, uses the default local database.
    """
    try:
        final_path = get_db_path(db_path)
        conn = sqlite3.connect(final_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]

        conn.close()
        if not tables:
            return "No tables found in this database."
        return f"Database: {os.path.basename(final_path)}\nTables found: {', '.join(tables)}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def describe_table(table_name: str, db_path: str = None) -> str:
    """
    Returns the schema for a specific table.
    Args:
        table_name: The name of the table to inspect.
        db_path: (Optional) Path to the .db file.
    """
    try:
        final_path = get_db_path(db_path)
        conn = sqlite3.connect(final_path)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        conn.close()

        if not columns:
            return f"Table '{table_name}' not found."

        schema_info = [f"Schema for {table_name} (in {os.path.basename(final_path)}):"]
        for col in columns:
            schema_info.append(f"- {col[1]} ({col[2]})")

        return "\n".join(schema_info)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def run_select_query(query: str, db_path: str = None) -> str:
    """
    Executes a SAFE, read-only SQL query.
    Args:
        query: The SQL query to run (SELECT only).
        db_path: (Optional) Path to the .db file.
    """
    if not query.strip().lower().startswith("select"):
        return "Error: Only SELECT queries are allowed."

    try:
        final_path = get_db_path(db_path)
        conn = sqlite3.connect(final_path)
        cursor = conn.cursor()

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return str(results)
    except Exception as e:
        return f"SQL Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
