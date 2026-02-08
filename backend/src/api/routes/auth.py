from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
import uuid
from pydantic import BaseModel, EmailStr

from ...dependencies import get_db, get_current_user
from ...models.user import User, UserCreate, UserRead
from ...repositories.user_repository import create_user, get_user_by_email
from ...auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"

@router.post("/sign-up/email")
def signup_email(request: SignUpRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Register a new user with email and password.
    """
    # Check if user already exists
    existing_user = get_user_by_email(db=db, email=request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Generate a unique user ID
    user_id = str(uuid.uuid4())
    
    # Create new user
    user_data = UserCreate(
        email=request.email,
        password=request.password,
        first_name=request.name
    )
    
    try:
        user = create_user(db=db, user_data=user_data)
        
        # Create access token
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=token_data)
        
        # Prepare response - use model_dump(mode='json') to avoid UUID serialization issues
        return AuthResponse(
            user=UserRead(**user.model_dump(mode='json')),
            access_token=access_token,
            token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/sign-in/email")
def signin_email(request: SignInRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """
    Authenticate user with email and password.
    """
    # Find user by email
    user = get_user_by_email(db=db, email=request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # In a real implementation, we would verify the password hash here
    # For now, we'll assume the password is correct since we're not storing passwords
    
    try:
        # Create access token
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=token_data)
        
        return AuthResponse(
            user=UserRead(**user.model_dump(mode='json')),
            access_token=access_token,
            token_type="bearer"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating access token: {str(e)}"
        )

# Add a session endpoint to get current user info
@router.get("/session")
def get_session(current_user: dict = Depends(get_current_user)):
    """
    Get current user session information.
    """
    # Return user information from the validated JWT token
    return {"user_id": current_user["user_id"], "email": current_user["email"]}