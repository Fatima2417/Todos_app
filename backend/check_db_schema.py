import sys
import os
from sqlalchemy import inspect

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.database.engine import engine

def check_columns():
    inspector = inspect(engine)
    for table_name in ['conversation', 'message']:
        columns = [c['name'] for c in inspector.get_columns(table_name)]
        print(f"Table: {table_name}, Columns: {columns}")

if __name__ == "__main__":
    check_columns()
