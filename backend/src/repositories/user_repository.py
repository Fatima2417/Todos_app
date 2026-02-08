from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate


def create_user(*, db: Session, user_data: UserCreate) -> User:
    """
    Create a new user.

    Args:
        db: Database session
        user_data: User creation data

    Returns:
        The created User object
    """
    # Prepare user data
    user_dict = user_data.model_dump() if hasattr(user_data, 'model_dump') else user_data.dict()
    
    # Extract password to create hashed_password
    password = user_dict.pop("password")
    # For now, we'll just use the password as the hash until we add a hashing library
    user_dict["hashed_password"] = f"plain:{password}"
    
    user = User(**user_dict)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(*, db: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.

    Args:
        db: Database session
        email: The email address to search for

    Returns:
        The user if found, None otherwise
    """
    query = select(User).where(User.email == email)
    return db.exec(query).first()


def get_user_by_id(*, db: Session, user_id: str) -> Optional[User]:
    """
    Get a user by their ID.

    Args:
        db: Database session
        user_id: The ID of the user to retrieve

    Returns:
        The user if found, None otherwise
    """
    query = select(User).where(User.id == user_id)
    return db.exec(query).first()
