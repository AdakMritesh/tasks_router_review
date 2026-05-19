"""
User management API endpoints for retrieving and creating users.
"""

from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session

from tasks_router.services.user_service import UserService
# from tasks_router.repositories.user_repo import UserRepository
from tasks_router.schema.user_schema import User
# from tasks_router.database.initiate_db import Database
# from tasks_router.database.config_db import settings
from tasks_router.dependencies import get_user_services

router: APIRouter = APIRouter(prefix="/users", tags=["Users"])

# _db = Database(settings)

@router.get(
        "/{username}",
        response_model=User,
        status_code=status.HTTP_200_OK)
def get_user(
    username: str,
    user_services: UserService = Depends(get_user_services)
    ) -> User:
    """Endpoint to retrieve a user by username."""
    
    user: User | None = user_services.get_user(username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post(
        "/",
        response_model=User,
        status_code=status.HTTP_201_CREATED
    )
def create_user(
    user: User,
    user_services: UserService = Depends(get_user_services)
    ) -> User:
    """Endpoint to create a new user."""

    return user_services.create(user)
