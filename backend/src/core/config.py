import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))

# Application configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
PROJECT_NAME = os.getenv("PROJECT_NAME", "Todo App API")
VERSION = "1.0.0"
API_V1_STR = "/api/v1"

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Validate required environment variables
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")