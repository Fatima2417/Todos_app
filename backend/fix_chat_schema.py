import sys
import os
from sqlalchemy import text

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.database.engine import engine
from src.database.init_db import initialize_database
from src.models import chat  # Ensure models are loaded

def fix_schema():
    print("Connecting to database...")
    with engine.connect() as connection:
        print("Dropping 'message' and 'conversation' tables to fix schema...")
        # Drop message first because it has a foreign key to conversation
        connection.execute(text("DROP TABLE IF EXISTS message CASCADE"))
        connection.execute(text("DROP TABLE IF EXISTS conversation CASCADE"))
        connection.commit()
    
    print("Recreating tables with correct schema...")
    initialize_database()
    print("Schema fix completed successfully!")

if __name__ == "__main__":
    try:
        fix_schema()
    except Exception as e:
        print(f"Error fixing schema: {e}")
        import traceback
        traceback.print_exc()
