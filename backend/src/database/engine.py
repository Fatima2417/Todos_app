from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Get the DATABASE_URL injected by the Neon Vercel Integration
database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# CRITICAL FOR SERVERLESS: Create a new engine for each request.
# Do NOT try to share or pool connections across requests.
# 'pool_pre_ping=True' helps check if a connection is alive before using it.
# 'pool_recycle=300' (seconds) is often needed to avoid stale connections.
engine = create_engine(
    database_url,
    echo=False,  # Set to True only for debugging in logs
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
)

# Function to get a fresh session per request
def get_session():
    return Session(engine)


def create_db_and_tables():
    """Create database tables based on SQLModel models"""
    SQLModel.metadata.create_all(engine)