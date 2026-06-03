import uuid

import structlog
from fastapi import Depends

from .dependencies import get_user_repository
from .repositories.user_repo import UserRepository

logger = structlog.get_logger(__name__)
MOCK_USER_ID: uuid.UUID | None = None

async def get_current_user_id(user_repository: UserRepository = Depends(get_user_repository)) -> uuid.UUID:
    """
    Placeholder function to simulate user authentication and retrieval of the current user's ID.
    """
    global MOCK_USER_ID
    
    if MOCK_USER_ID is not None:
        logger.debug("auth.mock_user.cached", user_id=str(MOCK_USER_ID))
        return MOCK_USER_ID
    
    logger.info("auth.mock_user.fetch")
    
    users = user_repository.get_all()
    MOCK_USER_ID = users[0].id
    
    logger.info("auth.mock_user.assigned", user_id=str(MOCK_USER_ID))
    return MOCK_USER_ID
