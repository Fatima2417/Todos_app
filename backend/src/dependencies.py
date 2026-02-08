from sqlmodel import Session
from fastapi import Depends, HTTPException, status, Request
from .database.session import get_session
from .auth.jwt import verify_token
from .models.user import User
from sqlmodel import select


def get_db():
    """
    FastAPI dependency that provides a database session.
    This ensures that each request gets a fresh session that's closed after the request.
    """
    yield from get_session()


def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    FastAPI dependency to get current user from either JWT token in Authorization header
    or from X-User-ID header (for Better Auth integration).
    Raises HTTPException(401) for invalid tokens or missing user.
    """
    # First, try to get user ID from the custom header (Better Auth approach)
    user_id = request.headers.get("x-user-id")
    
    if user_id:
        # Verify that the user exists in the database
        user = db.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, "email": user.email}
    
    # Fallback to JWT token approach
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>" format
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify the JWT token and extract payload
    payload = verify_token(token)
    
    # Extract user_id from the payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify that the user exists in the database
    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"user_id": user_id, "email": payload.get("email")}


def validate_user_path(path_user_id: str, current_user: dict = Depends(get_current_user)):
    """
    FastAPI dependency to validate that the user_id in the JWT token matches
    the user_id in the request path parameter.

    Args:
        path_user_id: User ID from the request path parameter
        current_user: User dictionary from JWT token via get_current_user dependency

    Returns:
        The validated user ID if it matches

    Raises:
        HTTPException: If the JWT user_id doesn't match the path user_id
    """
    jwt_user_id = current_user["user_id"]

    if str(jwt_user_id) != str(path_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in request path"
        )

    return path_user_id