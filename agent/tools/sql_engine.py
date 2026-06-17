# agent/tools/sql_engine.py
# SQL Tool — agent is se CSV data pe SQL queries run karta hai

import duckdb
import pandas as pd
from langchain.tools import Tool

# Global variable — CSV file path yahan store hoga
_csv_path = None
_dataframe = None

def set_csv_path(path: str, df: pd.DataFrame):
    """
    Jab user CSV upload kare, yeh function call hota hai.
    CSV path aur DataFrame store karta hai.
    """
    global _csv_path, _dataframe
    _csv_path = path
    _dataframe = df
    print(f"SQL Engine ready: {path}")

def run_sql_query(query: str) -> str:
    """
    Agent ka likha hua SQL query execute karta hai.
    DuckDB directly DataFrame pe query run karta hai.
    """
    global _dataframe
    
    if _dataframe is None:
        return "Error: Koi CSV upload nahi hua. Pehle CSV upload karo."
    
    try:
        # DuckDB connection banao (in-memory)
        conn = duckdb.connect()
        
        # DataFrame ko 'data' table ke roop mein register karo
        conn.register("data", _dataframe)
        
        # Query run karo
        result = conn.execute(query).fetchdf()
        
        # Connection close karo
        conn.close()
        
        # Result return karo (max 20 rows)
        if len(result) > 20:
            return f"{result.head(20).to_string()}\n\n... aur {len(result)-20} rows hain."
        
        return result.to_string()
    
    except Exception as e:
        return f"SQL Error: {str(e)}"

# LangChain Tool object banao
sql_tool = Tool(
    name="SQL_Engine",
    description="""
    CSV data pe SQL queries run karne ke liye use karo.
    Table ka naam 'data' hai.
    
    Example queries:
    SELECT * FROM data LIMIT 5
    SELECT Category, SUM(Sales) FROM data GROUP BY Category
    SELECT * FROM data WHERE Sales > 1000 ORDER BY Sales DESC
    """,
    func=run_sql_query
)