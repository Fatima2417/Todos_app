from .engine import create_db_and_tables


def initialize_database():
    """
    Initialize the database by creating all required tables.
    This should be called once during application startup.
    """
    create_db_and_tables()
    print("Database tables created successfully.")