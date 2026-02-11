from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api.routes.tasks import router as tasks_router
from src.api.routes.auth import router as auth_router
from src.api.chat import router as chat_router
from src.core.config import PROJECT_NAME, VERSION, API_V1_STR, DEBUG
from src.database.init_db import initialize_database
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler to manage application startup and shutdown events.
    """
    # Startup: Initialize database tables
    print("Initializing database...")
    initialize_database()
    print("Database initialized successfully!")
    
    yield  # Application runs during this period
    
    # Shutdown: Cleanup code would go here if needed
    print("Shutting down...")


# Create the FastAPI application instance
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    debug=DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register the auth routes under the root path
app.include_router(auth_router, prefix="")

# Register the chat router
app.include_router(chat_router, prefix="")

# Register the API routes under the v1 prefix
app.include_router(tasks_router, prefix=API_V1_STR + "/{path_user_id}", tags=["todo-tasks"])


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": f"Welcome to the {PROJECT_NAME} API", "version": VERSION}


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy", "message": "Todo API is running successfully"}