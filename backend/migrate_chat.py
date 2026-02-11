import sys
import os

# Add the current directory to sys.path to allow imports from src
sys.path.append(os.path.join(os.getcwd(), 'src'))

from src.database.init_db import initialize_database
from src.models import chat  # Ensure chat models are imported so SQLModel knows about them

if __name__ == "__main__":
    print("Running migration for chat tables...")
    initialize_database()
    print("Migration completed.")
